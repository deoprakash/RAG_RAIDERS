from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class CIMonitorAgent:
    timeline: list[dict] = field(default_factory=list)

    def record(self, iteration: int, status: str) -> None:
        self.timeline.append(
            {
                "iteration": iteration,
                "status": status,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )
