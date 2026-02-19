# backend>utils>file_editor.py
from __future__ import annotations

from pathlib import Path
from typing import Callable


def safe_read_lines(file_path: Path) -> list[str]:
    return file_path.read_text(encoding="utf-8").splitlines(keepends=True)


def safe_write_lines(file_path: Path, lines: list[str]) -> None:
    file_path.write_text("".join(lines), encoding="utf-8")


def remove_line(file_path: Path, line_number: int) -> bool:
    lines = safe_read_lines(file_path)
    index = line_number - 1
    if index < 0 or index >= len(lines):
        return False
    del lines[index]
    safe_write_lines(file_path, lines)
    return True


def update_line(file_path: Path, line_number: int, updater: Callable[[str], str]) -> bool:
    lines = safe_read_lines(file_path)
    index = line_number - 1
    if index < 0 or index >= len(lines):
        return False
    lines[index] = updater(lines[index])
    safe_write_lines(file_path, lines)
    return True


def insert_line(file_path: Path, line_number: int, content: str) -> bool:
    lines = safe_read_lines(file_path)
    index = max(0, min(line_number - 1, len(lines)))
    insert_value = content if content.endswith("\n") else f"{content}\n"
    lines.insert(index, insert_value)
    safe_write_lines(file_path, lines)
    return True


def normalize_indentation(file_path: Path) -> bool:
    lines = safe_read_lines(file_path)
    normalized = []
    for line in lines:
        stripped = line.lstrip(" \t")
        prefix = line[: len(line) - len(stripped)]
        spaces = prefix.replace("\t", "    ")
        normalized.append(spaces + stripped)
    safe_write_lines(file_path, normalized)
    return True

