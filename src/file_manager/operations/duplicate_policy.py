from __future__ import annotations

from enum import Enum
from pathlib import Path

from file_manager.utils.hashing import hash_file
from file_manager.utils.paths import unique_destination_path


class DuplicateHandling(str, Enum):
    SKIP = "skip"
    OVERWRITE = "overwrite"
    RENAME = "rename"
    HASH_COMPARE_SKIP = "hash-compare-skip"


def resolve_destination(source: Path, destination: Path, policy: DuplicateHandling) -> tuple[Path | None, str]:
    if not destination.exists():
        return destination, "new"

    if policy == DuplicateHandling.SKIP:
        return None, "skipped-existing"

    if policy == DuplicateHandling.OVERWRITE:
        return destination, "overwrite"

    if policy == DuplicateHandling.RENAME:
        return unique_destination_path(destination), "renamed"

    if policy == DuplicateHandling.HASH_COMPARE_SKIP:
        try:
            if hash_file(source) == hash_file(destination):
                return None, "skipped-same-content"
            return unique_destination_path(destination), "renamed-different-content"
        except OSError:
            return unique_destination_path(destination), "renamed-after-hash-error"

    return None, "unknown"
