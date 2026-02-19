from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

try:
    from ..utils.bug_mapper import map_error_to_bug_type
except ImportError:
    from utils.bug_mapper import map_error_to_bug_type  # type: ignore


@dataclass
class ParsedFailure:
    file: str
    line_number: int
    message: str
    bug_type: str


class ErrorParserAgent:
    # Matches pytest-style source location lines: path.py:line: message
    PYTEST_LINE_RE = re.compile(
        r"^(?P<file>[^\s:][^:]*\.py):(?P<line>\d+):\s*(?P<message>.+)$"
    )

    # Captures traceback error payload lines prefixed with "E   ..."
    TRACEBACK_LINE_RE = re.compile(r"^E\s+(.+)$")

    def parse(self, output: str, repo_path: Path) -> list[ParsedFailure]:
        failures: list[ParsedFailure] = []
        lines = output.splitlines()

        for idx, line in enumerate(lines):
            match = self.PYTEST_LINE_RE.match(line.strip())
            if not match:
                continue

            raw_file = match.group("file")
            line_number = int(match.group("line"))
            message = match.group("message")

            # Attach traceback context if present
            if idx + 1 < len(lines):
                trace_match = self.TRACEBACK_LINE_RE.match(lines[idx + 1].strip())
                if trace_match:
                    message = f"{message} | {trace_match.group(1)}"

            normalized_file = self._normalize_file(raw_file, repo_path)

            # 🔥 CRITICAL FIX: ignore non-repo files (pytest, venv, site-packages)
            if not normalized_file:
                continue
            if normalized_file.startswith(".."):
                continue
            if normalized_file.startswith(".venv"):
                continue
            if "site-packages" in normalized_file:
                continue

            mapped = map_error_to_bug_type(message)

            failures.append(
                ParsedFailure(
                    file=normalized_file,
                    line_number=line_number,
                    message=message,
                    bug_type=mapped.bug_type,
                )
            )

        if failures:
            return self._dedupe(failures)

        # Best-effort fallback (rare, but safe)
        fallback_message = self._best_effort_message(lines)
        if fallback_message:
            mapped = map_error_to_bug_type(fallback_message)
            failures.append(
                ParsedFailure(
                    file="",
                    line_number=0,
                    message=fallback_message,
                    bug_type=mapped.bug_type,
                )
            )

        return failures

    def _normalize_file(self, file_path: str, repo_path: Path) -> str:
        """
        Normalize paths so only repo-relative paths are returned.
        Absolute paths outside repo are rejected.
        """
        path = Path(file_path)

        if path.is_absolute():
            try:
                return str(path.relative_to(repo_path))
            except ValueError:
                return ""

        return file_path

    def _best_effort_message(self, lines: list[str]) -> str:
        for line in lines:
            if "Error" in line or "FAILED" in line or "assert" in line.lower():
                return line.strip()
        return ""

    def _dedupe(self, failures: list[ParsedFailure]) -> list[ParsedFailure]:
        seen: set[tuple[str, int, str]] = set()
        unique: list[ParsedFailure] = []

        for failure in failures:
            key = (failure.file, failure.line_number, failure.bug_type)
            if key in seen:
                continue
            seen.add(key)
            unique.append(failure)

        return unique
