from __future__ import annotations

import subprocess
from pathlib import Path


class GitAgent:
    def __init__(self, repo_path: Path) -> None:
        self.repo_path = repo_path

    def create_branch(self, branch_name: str) -> None:
        subprocess.run(
            ["git", "checkout", "-b", branch_name],
            cwd=self.repo_path,
            check=True,
        )

    def commit_fix(self, file_path: str, commit_message: str) -> bool:
        subprocess.run(["git", "add", file_path], cwd=self.repo_path, check=True)

        check = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=self.repo_path,
        )
        if check.returncode == 0:
            return False

        subprocess.run(
            ["git", "commit", "-m", f"[AI-AGENT] {commit_message}"],
            cwd=self.repo_path,
            check=True,
        )
        return True

    def push_branch(self, branch_name: str) -> None:
        subprocess.run(
            ["git", "push", "-u", "origin", branch_name],
            cwd=self.repo_path,
            check=True,
        )
