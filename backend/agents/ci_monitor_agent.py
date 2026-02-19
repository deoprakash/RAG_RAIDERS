from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class CIMonitorAgent:
    timeline: list[dict] = field(default_factory=list)

    def record(self, iteration: int, status: str, failures_remaining: int | None = None) -> None:
        event = {
            "iteration": iteration,
            "status": status,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        if failures_remaining is not None:
            event["failures_remaining"] = failures_remaining
        self.timeline.append(event)
