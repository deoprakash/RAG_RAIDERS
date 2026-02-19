from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class DevOpsAutomationBridge:
    def __init__(self, branch_history_path: Path, ci_timeline_path: Path) -> None:
        self.branch_history_path = branch_history_path
        self.ci_timeline_path = ci_timeline_path

    def sync_run_data(
        self,
        *,
        branch_name: str,
        team_name: str,
        leader_name: str,
        ci_timeline: list[dict[str, Any]],
    ) -> None:
        self._append_branch_history(branch_name=branch_name, team_name=team_name, leader_name=leader_name)
        self._update_ci_timeline(ci_timeline=ci_timeline)

    def _append_branch_history(self, *, branch_name: str, team_name: str, leader_name: str) -> None:
        history = self._read_json_array(self.branch_history_path)
        history.append(
            {
                "branch_name": branch_name,
                "type": "fix",
                "timestamp": datetime.now().isoformat(),
                "issue_id": "N/A",
                "description": f"Auto run for {team_name} / {leader_name}",
                "created_by": "backend_coordinator",
                "status": "created",
            }
        )
        self._write_json(self.branch_history_path, history)

    def _update_ci_timeline(self, *, ci_timeline: list[dict[str, Any]]) -> None:
        now = datetime.now().isoformat()
        payload = {
            "project": "RIFT'26 - DevOps Lead",
            "start_time": ci_timeline[0]["timestamp"] if ci_timeline else now,
            "end_time": ci_timeline[-1]["timestamp"] if ci_timeline else now,
            "total_iterations": len(ci_timeline),
            "pipeline_history": [
                {
                    "iteration": item.get("iteration", idx + 1),
                    "start_time": item.get("timestamp", now),
                    "mode": "backend",
                    "stages": {
                        "test": {
                            "passed": item.get("status", "FAILED") == "PASSED",
                            "timestamp": item.get("timestamp", now),
                            "simulated": False,
                        }
                    },
                    "duration": 0,
                    "status": str(item.get("status", "FAILED")).lower(),
                    "end_time": item.get("timestamp", now),
                }
                for idx, item in enumerate(ci_timeline)
            ],
        }
        self._write_json(self.ci_timeline_path, payload)

    def _read_json_array(self, path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []

        raw = path.read_text(encoding="utf-8").strip()
        if not raw:
            return []

        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return parsed
        return []

    def _write_json(self, path: Path, payload: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
