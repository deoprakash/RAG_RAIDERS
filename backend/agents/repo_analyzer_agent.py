# backend>agents>repo_analyzer_agent.py
from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
import time



@dataclass
class RepoAnalysis:
    repo_path: Path
    discovered_tests: list[str]


class RepoAnalyzerAgent:
    def __init__(self, workspaces_dir: Path) -> None:
        self.workspaces_dir = workspaces_dir

    def clone_and_analyze(self, repo_url: str, target_dir_name: str) -> RepoAnalysis:
        self.workspaces_dir.mkdir(parents=True, exist_ok=True)
        repo_path = self.workspaces_dir / target_dir_name

        if repo_path.exists():
            try:
                shutil.rmtree(repo_path)
            except PermissionError:
                #windows file lock fallback
                time.sleep(1)
                shutil.rmtree(repo_path, ignore_errors=True)
            

        subprocess.run(["git", "clone", repo_url, str(repo_path)], check=True)
        discovered_tests = self._discover_tests(repo_path)
        return RepoAnalysis(repo_path=repo_path, discovered_tests=discovered_tests)

    def _discover_tests(self, repo_path: Path) -> list[str]:
        tests: list[str] = []
        for path in repo_path.rglob("*.py"):
            name = path.name
            if name.startswith("test") or name.endswith("_test.py"):
                tests.append(str(path.relative_to(repo_path)))
        return sorted(set(tests))

