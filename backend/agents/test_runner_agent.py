# backend>agents>test_runner_agent.py
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

try:
    from ..config import PYTEST_TIMEOUT_SECONDS
except ImportError:
    from config import PYTEST_TIMEOUT_SECONDS  # type: ignore


@dataclass
class TestRunResult:
    passed: bool
    output: str
    return_code: int


class TestRunnerAgent:
    def run(self, repo_path: Path, tests: list[str]) -> TestRunResult:
        cmd = ["pytest", "-q"]
        if tests:
            cmd.extend(tests)

        proc = subprocess.run(
            cmd,
            cwd=repo_path,
            text=True,
            capture_output=True,
            timeout=PYTEST_TIMEOUT_SECONDS,
        )
        output = f"{proc.stdout}\n{proc.stderr}".strip()
        return TestRunResult(passed=proc.returncode == 0, output=output, return_code=proc.returncode)

