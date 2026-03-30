from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class DuplicateGroup:
    group_id: str
    hash_algorithm: str
    hash_value: str
    size_bytes: int
    files: list[Path] = field(default_factory=list)
