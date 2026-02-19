# backend>scoring.py
from __future__ import annotations

from dataclasses import dataclass

try:
    from .config import (
        BASE_SCORE,
        COMMIT_PENALTY_PER_EXTRA_COMMIT,
        COMMIT_PENALTY_THRESHOLD,
        SPEED_BONUS_POINTS,
        SPEED_BONUS_THRESHOLD_SECONDS,
    )
except ImportError:
    from config import (  # type: ignore
        BASE_SCORE,
        COMMIT_PENALTY_PER_EXTRA_COMMIT,
        COMMIT_PENALTY_THRESHOLD,
        SPEED_BONUS_POINTS,
        SPEED_BONUS_THRESHOLD_SECONDS,
    )


@dataclass
class ScoreBreakdown:
    base: int
    speed_bonus: int
    penalty: int
    final_score: int


def calculate_score(time_taken_seconds: float, commit_count: int) -> ScoreBreakdown:
    base = BASE_SCORE
    speed_bonus = SPEED_BONUS_POINTS if time_taken_seconds < SPEED_BONUS_THRESHOLD_SECONDS else 0

    extra_commits = max(0, commit_count - COMMIT_PENALTY_THRESHOLD)
    penalty = extra_commits * COMMIT_PENALTY_PER_EXTRA_COMMIT

    final_score = max(0, base + speed_bonus - penalty)
    return ScoreBreakdown(
        base=base,
        speed_bonus=speed_bonus,
        penalty=penalty,
        final_score=final_score,
    )

