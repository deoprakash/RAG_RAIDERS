# backend>agents>test_runner_agent.py
from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from ..config import PYTEST_TIMEOUT_SECONDS, SANDBOX_DOCKER_IMAGE, SANDBOX_WORKDIR
except ImportError:
    from config import PYTEST_TIMEOUT_SECONDS, SANDBOX_DOCKER_IMAGE, SANDBOX_WORKDIR  # type: ignore


@dataclass
class TestRunResult:
    passed: bool
    output: str
    return_code: int


class TestRunnerAgent:
    def run(self, repo_path: Path, tests: list[str]) -> TestRunResult:
        if shutil.which("docker") is None:
            return TestRunResult(
                passed=False,
                output="Sandbox enforcement active: Docker is required but not available on PATH.",
                return_code=127,
            )

        install_steps = [
            "python -m pip install -q --upgrade pip pytest",
        ]

        for requirements_file in [
            "requirements.txt",
            "requirements-dev.txt",
            "dev-requirements.txt",
        ]:
            if (repo_path / requirements_file).exists():
                install_steps.append(
                    f"python -m pip install -q -r {shlex.quote(requirements_file)}"
                )

        pytest_cmd = ["python", "-m", "pytest", "-q"]
        if tests:
            pytest_cmd.extend(tests)

        sandbox_script = " && ".join(install_steps + [shlex.join(pytest_cmd)])

        # Use a named volume so pip cache is reused across retries — avoids
        # re-downloading packages on every Docker container start.
        pip_cache_volume = "rift2026_pip_cache"

        cmd = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{os.fspath(repo_path)}:{SANDBOX_WORKDIR}",
            "-v",
            f"{pip_cache_volume}:/root/.cache/pip",
            "-w",
            SANDBOX_WORKDIR,
            SANDBOX_DOCKER_IMAGE,
            "sh",
            "-lc",
            sandbox_script,
        ]

        try:
            proc = subprocess.run(
                cmd,
                cwd=repo_path,
                text=True,
                capture_output=True,
                timeout=PYTEST_TIMEOUT_SECONDS,
            )
            output = f"{proc.stdout}\n{proc.stderr}".strip()
            return TestRunResult(
                passed=proc.returncode == 0,
                output=output,
                return_code=proc.returncode,
            )
        except subprocess.TimeoutExpired as exc:
            timed_output = f"{exc.stdout or ''}\n{exc.stderr or ''}".strip()
            message = (
                f"Sandboxed pytest timed out after {PYTEST_TIMEOUT_SECONDS} seconds."
            )
            output = f"{timed_output}\n{message}".strip()
            return TestRunResult(passed=False, output=output, return_code=124)

