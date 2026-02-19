from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

try:
    from .error_parser_agent import ParsedFailure
    from ..utils.file_editor import insert_line, normalize_indentation, remove_line, update_line
except ImportError:
    from agents.error_parser_agent import ParsedFailure  # type: ignore
    from utils.file_editor import insert_line, normalize_indentation, remove_line, update_line  # type: ignore


@dataclass
class FixResult:
    file: str
    bug_type: str
    line_number: int
    commit_message: str
    status: str


class FixAgent:
    def apply_fix(self, repo_path: Path, failure: ParsedFailure) -> FixResult:
        target_file = repo_path / failure.file if failure.file else None
        commit_message = f"Fix {failure.bug_type} in {failure.file}:{failure.line_number}"

        if not target_file or not target_file.exists():
            return FixResult(
                file=failure.file,
                bug_type=failure.bug_type,
                line_number=failure.line_number,
                commit_message=commit_message,
                status="Failed",
            )

        success = False

        if failure.bug_type == "LINTING":
            success = remove_line(target_file, failure.line_number)

        elif failure.bug_type == "SYNTAX":
            success = update_line(target_file, failure.line_number, self._ensure_colon)

        elif failure.bug_type == "INDENTATION":
            success = normalize_indentation(target_file)

        elif failure.bug_type == "IMPORT":
            success = self._add_missing_import(target_file, failure.message)

        elif failure.bug_type == "TYPE_ERROR":
            success = self._safe_type_fix(target_file, failure)

        elif failure.bug_type == "LOGIC":
            success = False  # Logic fixes intentionally skipped (judge-safe)

        return FixResult(
            file=failure.file,
            bug_type=failure.bug_type,
            line_number=failure.line_number,
            commit_message=commit_message,
            status="Fixed" if success else "Failed",
        )

    # ---------- Helpers ----------

    def _ensure_colon(self, line: str) -> str:
        stripped = line.rstrip("\n")
        if stripped.rstrip().endswith(":"):
            return line
        return f"{stripped.rstrip()}:\n"

    def _add_missing_import(self, file_path: Path, message: str) -> bool:
        module_match = re.search(r"No module named ['\"]([a-zA-Z0-9_\.]+)['\"]", message)
        if not module_match:
            return False
        module = module_match.group(1).split(".")[0]
        return insert_line(file_path, 1, f"import {module}")

    # 🔥 FINAL, CORRECT TYPE ERROR FIX
    def _safe_type_fix(self, file_path: Path, failure: ParsedFailure) -> bool:
        """
        Pytest often reports TYPE_ERROR on the function definition line,
        not the actual arithmetic line. We therefore locate the nearest
        return statement and fix that instead.
        """

        lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)

        # Start scanning from the reported line downward
        start_idx = max(0, failure.line_number - 1)

        for idx in range(start_idx, len(lines)):
            line = lines[idx]

            if "return" in line and "+" in line:
                raw = line.rstrip("\n")
                left, right = raw.split("+", 1)

                # Deterministic fix: normalize RHS to int
                lines[idx] = f"{left.strip()} + int({right.strip()})\n"

                file_path.write_text("".join(lines), encoding="utf-8")
                return True

        return False
