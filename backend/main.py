# backend>main.py
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

try:
    from .config import DEFAULT_MAX_RETRY
    from .coordinator import AgentCoordinator, load_results
except ImportError:
    from config import DEFAULT_MAX_RETRY  # type: ignore
    from coordinator import AgentCoordinator, load_results  # type: ignore


app = FastAPI(title="RIFT 2026 Autonomous Agent Backend", version="1.0.0")
coordinator = AgentCoordinator()


class RunAgentRequest(BaseModel):
    repo_url: str = Field(..., min_length=1)
    team_name: str = Field(..., min_length=1)
    leader_name: str = Field(..., min_length=1)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/results")
def get_results() -> dict:
    return load_results()


@app.post("/run-agent")
def run_agent(payload: RunAgentRequest) -> dict:
    try:
        return coordinator.execute(
            repo_url=payload.repo_url,
            team_name=payload.team_name,
            leader_name=payload.leader_name,
            max_retry=DEFAULT_MAX_RETRY,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {exc}") from exc

