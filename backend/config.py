# backend>config.py
from __future__ import annotations

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
RESULTS_PATH = BASE_DIR / "results" / "results.json"
WORKSPACES_DIR = BASE_DIR / "workspaces"

DEFAULT_MAX_RETRY = 5
PYTEST_TIMEOUT_SECONDS = 180

BASE_SCORE = 100
SPEED_BONUS_THRESHOLD_SECONDS = 300
SPEED_BONUS_POINTS = 10
COMMIT_PENALTY_THRESHOLD = 20
COMMIT_PENALTY_PER_EXTRA_COMMIT = 2

