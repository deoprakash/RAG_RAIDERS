# backend>config.py
from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
RESULTS_PATH = BASE_DIR / "results" / "results.json"
WORKSPACES_DIR = BASE_DIR / "workspaces"
DEVOPS_AUTOMATION_DIR = ROOT_DIR / "DevOps_Git_Automation"
DEVOPS_DATA_DIR = DEVOPS_AUTOMATION_DIR / "data"
DEVOPS_BRANCH_HISTORY_PATH = DEVOPS_DATA_DIR / "branch_history.json"
DEVOPS_CI_TIMELINE_PATH = DEVOPS_DATA_DIR / "ci_pipeline_timeline.json"

DEFAULT_MAX_RETRY = 5
PYTEST_TIMEOUT_SECONDS = 180
SANDBOX_DOCKER_IMAGE = "python:3.11-slim"
SANDBOX_WORKDIR = "/workspace"

BASE_SCORE = 100
SPEED_BONUS_THRESHOLD_SECONDS = 300
SPEED_BONUS_POINTS = 10
COMMIT_PENALTY_THRESHOLD = 20
COMMIT_PENALTY_PER_EXTRA_COMMIT = 2

