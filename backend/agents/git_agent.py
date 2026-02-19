from __future__ import annotations

import os
import subprocess
from pathlib import Path


class GitAgent:
    def __init__(self, repo_path: Path) -> None:
        self.repo_path = repo_path
        self.env = os.environ.copy()
        self.env["GIT_TERMINAL_PROMPT"] = "0"
        self.env["GIT_SSH_COMMAND"] = "ssh -o BatchMode=yes"

    def _with_ai_prefix(self, message: str) -> str:
        if message.startswith("[AI-AGENT]"):
            return message
        return f"[AI-AGENT] {message}"

    def create_branch(self, branch_name: str) -> None:
        subprocess.run(
            ["git", "checkout", "-b", branch_name],
            cwd=self.repo_path,
            check=True,
            timeout=30,
            env=self.env,
        )

    def commit_fix(self, file_path: str, commit_message: str) -> bool:
        subprocess.run(
            ["git", "add", file_path],
            cwd=self.repo_path,
            check=True,
            timeout=30,
            env=self.env,
        )

        check = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=self.repo_path,
            timeout=30,
            env=self.env,
        )
        if check.returncode == 0:
            return False

        subprocess.run(
            ["git", "commit", "-m", self._with_ai_prefix(commit_message)],
            cwd=self.repo_path,
            check=True,
            timeout=30,
            env=self.env,
        )
        return True

    def push_branch(self, branch_name: str) -> None:
        subprocess.run(
            ["git", "push", "-u", "origin", branch_name],
            cwd=self.repo_path,
            check=True,
            timeout=120,
            env=self.env,
        )
