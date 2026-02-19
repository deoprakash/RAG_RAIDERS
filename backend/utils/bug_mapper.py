# backend>utils>bug_mapper.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


ERROR_RULES = [
    {"pattern": "unused import", "bug_type": "LINTING"},
    {"pattern": "Missing colon", "bug_type": "SYNTAX"},
    {"pattern": "IndentationError", "bug_type": "INDENTATION"},
    {"pattern": "ModuleNotFoundError", "bug_type": "IMPORT"},
    {"pattern": "TypeError", "bug_type": "TYPE_ERROR"},
]

ALLOWED_BUG_TYPES = {"LINTING", "SYNTAX", "LOGIC", "TYPE_ERROR", "IMPORT", "INDENTATION"}


@dataclass
class MappedBug:
    bug_type: str
    matched_pattern: str | None


def map_error_to_bug_type(message: str) -> MappedBug:
    lowered = message.lower()
    for rule in ERROR_RULES:
        if rule["pattern"].lower() in lowered:
            return MappedBug(bug_type=rule["bug_type"], matched_pattern=rule["pattern"])

    if "assert" in lowered:
        return MappedBug(bug_type="LOGIC", matched_pattern="assert")

    return MappedBug(bug_type="LOGIC", matched_pattern=None)


def is_allowed_bug_type(bug_type: str) -> bool:
    return bug_type in ALLOWED_BUG_TYPES


def normalize_bug_types(items: Iterable[str]) -> list[str]:
    return [bug for bug in items if is_allowed_bug_type(bug)]

