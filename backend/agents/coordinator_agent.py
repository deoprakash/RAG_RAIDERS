from __future__ import annotations

import json
import re
import time
from typing import Any

try:
    from .ci_monitor_agent import CIMonitorAgent
    from .error_parser_agent import ErrorParserAgent
    from .fix_agent import FixAgent
    from .git_agent import GitAgent
    from .repo_analyzer_agent import RepoAnalyzerAgent
    from .test_runner_agent import TestRunnerAgent
    from ..config import (
        DEVOPS_BRANCH_HISTORY_PATH,
        DEVOPS_CI_TIMELINE_PATH,
        DEVOPS_DATA_DIR,
        RESULTS_PATH,
        WORKSPACES_DIR,
    )
    from ..scoring import calculate_score
    from ..utils.devops_bridge import DevOpsAutomationBridge
    from ..utils.logger import ensure_parent_dir, get_logger
except ImportError:
    from agents.ci_monitor_agent import CIMonitorAgent  # type: ignore
    from agents.error_parser_agent import ErrorParserAgent  # type: ignore
    from agents.fix_agent import FixAgent  # type: ignore
    from agents.git_agent import GitAgent  # type: ignore
    from agents.repo_analyzer_agent import RepoAnalyzerAgent  # type: ignore
    from agents.test_runner_agent import TestRunnerAgent  # type: ignore
    from config import (  # type: ignore
        DEVOPS_BRANCH_HISTORY_PATH,
        DEVOPS_CI_TIMELINE_PATH,
        DEVOPS_DATA_DIR,
        RESULTS_PATH,
        WORKSPACES_DIR,
    )
    from scoring import calculate_score  # type: ignore
    from utils.devops_bridge import DevOpsAutomationBridge  # type: ignore
    from utils.logger import ensure_parent_dir, get_logger  # type: ignore


class CoordinatorAgent:
    def __init__(self) -> None:
        self.logger = get_logger("CoordinatorAgent")
        self.repo_analyzer = RepoAnalyzerAgent(WORKSPACES_DIR)
        self.test_runner = TestRunnerAgent()
        self.error_parser = ErrorParserAgent()
        self.fix_agent = FixAgent()
        self.ci_monitor = CIMonitorAgent()
        self.devops_bridge = None

        if DEVOPS_DATA_DIR.exists():
            self.devops_bridge = DevOpsAutomationBridge(
                branch_history_path=DEVOPS_BRANCH_HISTORY_PATH,
                ci_timeline_path=DEVOPS_CI_TIMELINE_PATH,
            )

    def run(
        self,
        repo_url: str,
        team_name: str,
        leader_name: str,
        max_retry: int = 5,
    ) -> dict[str, Any]:
        start = time.monotonic()
        self.ci_monitor.timeline.clear()
        fixes: list[dict[str, Any]] = []
        total_failures = 0
        commit_count = 0
        final_status = "FAILED"
        stop_reason = "unknown"
        error_message = ""

        branch_name = self._build_branch_name(team_name, leader_name)

        # ✅ Unique workspace per run (Windows-safe, CI-safe)
        base_workspace = self._build_workspace_name(team_name, leader_name)
        workspace_name = f"{base_workspace}_{int(time.time())}"

        try:
            analysis = self.repo_analyzer.clone_and_analyze(repo_url, workspace_name)
            git_agent = GitAgent(analysis.repo_path)
            git_agent.create_branch(branch_name)

            consecutive_unparseable = 0

            for iteration in range(1, max_retry + 1):
                run_result = self.test_runner.run(
                    analysis.repo_path, analysis.discovered_tests
                )

                run_status = "PASSED" if run_result.passed else "FAILED"
                parsed_failures = []
                if not run_result.passed:
                    parsed_failures = self.error_parser.parse(
                        run_result.output, analysis.repo_path
                    )

                self.ci_monitor.record(
                    iteration=iteration,
                    status=run_status,
                    failures_remaining=len(parsed_failures),
                )

                # ✅ CI passed — stop immediately
                if run_result.passed:
                    final_status = "PASSED"
                    stop_reason = "tests_passed"
                    break

                total_failures += len(parsed_failures)

                if not parsed_failures:
                    consecutive_unparseable += 1
                    self.logger.warning(
                        "Test run failed but no parseable failures were found in iteration %s "
                        "(consecutive: %s)",
                        iteration,
                        consecutive_unparseable,
                    )
                    # After 2 consecutive unparseable failures there is nothing
                    # the agent can fix — bail out immediately instead of
                    # burning through all remaining retries.
                    if consecutive_unparseable >= 2:
                        self.logger.warning(
                            "Stopping retries: 2 consecutive unparseable failures."
                        )
                        stop_reason = "unparseable_failures"
                        break
                    continue
                else:
                    consecutive_unparseable = 0  # reset when we find actionable failures

                for failure in parsed_failures:
                    fix = self.fix_agent.apply_fix(analysis.repo_path, failure)

                    if fix.status == "Fixed":
                        try:
                            committed = git_agent.commit_fix(
                                fix.file, fix.commit_message
                            )
                            if committed:
                                commit_count += 1
                            else:
                                fix.status = "Failed"
                        except Exception as exc:
                            self.logger.exception("Commit failed: %s", exc)
                            fix.status = "Failed"

                    fixes.append(
                        {
                            "file": fix.file,
                            "bug_type": fix.bug_type,
                            "line_number": fix.line_number,
                            "commit_message": fix.commit_message,
                            "status": fix.status,
                        }
                    )

            if commit_count > 0:
                git_agent.push_branch(branch_name)

            if final_status != "PASSED":
                stop_reason = "max_retry_exhausted"

        except Exception as exc:
            self.logger.exception("Coordinator run failed: %s", exc)
            final_status = "FAILED"
            stop_reason = "runtime_error"
            error_message = str(exc)

        elapsed = time.monotonic() - start
        score = calculate_score(
            time_taken_seconds=elapsed, commit_count=commit_count
        )

        result: dict[str, Any] = {
            "repo_url": repo_url,
            "team_name": team_name,
            "leader_name": leader_name,
            "branch_name": branch_name,
            "total_failures": total_failures,
            "fixes_applied": sum(1 for f in fixes if f["status"] == "Fixed"),
            "final_status": final_status,
            "stop_reason": stop_reason,
            "error_message": error_message,
            "time_taken_seconds": round(elapsed, 3),
            "score": {
                "base": score.base,
                "speed_bonus": score.speed_bonus,
                "penalty": score.penalty,
                "final_score": score.final_score,
            },
            "fixes": fixes,
            "ci_cd_timeline": self.ci_monitor.timeline,
        }

        ensure_parent_dir(RESULTS_PATH)
        RESULTS_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")

        if self.devops_bridge is not None:
            try:
                self.devops_bridge.sync_run_data(
                    branch_name=branch_name,
                    team_name=team_name,
                    leader_name=leader_name,
                    ci_timeline=self.ci_monitor.timeline,
                )
            except Exception as exc:  # noqa: BLE001
                self.logger.exception(
                    "Failed to sync DevOps_Git_Automation data: %s", exc
                )

        return result

    def _build_branch_name(self, team_name: str, leader_name: str) -> str:
        safe_team = re.sub(r"[^A-Za-z0-9]+", "_", team_name.strip()).strip("_").upper()
        safe_leader = re.sub(r"[^A-Za-z0-9]+", "_", leader_name.strip()).strip("_").upper()
        return f"{safe_team}_{safe_leader}_AI_Fix"

    def _build_workspace_name(self, team_name: str, leader_name: str) -> str:
        safe_team = re.sub(r"[^A-Za-z0-9]+", "_", team_name.strip()).strip("_")
        safe_leader = re.sub(r"[^A-Za-z0-9]+", "_", leader_name.strip()).strip("_")
        return f"{safe_team}_{safe_leader}"
