# backend>coordinator.py
from __future__ import annotations

import json
from typing import Any

try:
    from .agents.coordinator_agent import CoordinatorAgent
    from .config import DEFAULT_MAX_RETRY, RESULTS_PATH
except ImportError:
    from agents.coordinator_agent import CoordinatorAgent  # type: ignore
    from config import DEFAULT_MAX_RETRY, RESULTS_PATH  # type: ignore


class AgentCoordinator:
    def __init__(self) -> None:
        self.agent = CoordinatorAgent()

    def execute(self, repo_url: str, team_name: str, leader_name: str, max_retry: int = DEFAULT_MAX_RETRY) -> dict[str, Any]:
        return self.agent.run(
            repo_url=repo_url,
            team_name=team_name,
            leader_name=leader_name,
            max_retry=max_retry,
        )


def load_results() -> dict[str, Any]:
    if not RESULTS_PATH.exists():
        return {
            "repo_url": "",
            "team_name": "",
            "leader_name": "",
            "branch_name": "TEAM_NAME_LEADER_NAME_AI_Fix",
            "total_failures": 0,
            "fixes_applied": 0,
            "final_status": "FAILED",
            "time_taken_seconds": 0,
            "score": {
                "base": 100,
                "speed_bonus": 0,
                "penalty": 0,
                "final_score": 0,
            },
            "fixes": [],
            "ci_cd_timeline": [],
        }
    return json.loads(RESULTS_PATH.read_text(encoding="utf-8"))

