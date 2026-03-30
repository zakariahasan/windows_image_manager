from __future__ import annotations

import shutil
from pathlib import Path


def get_free_disk_bytes(path: Path) -> int:
    usage = shutil.disk_usage(path)
    return usage.free


def has_enough_disk_space(destination_root: Path, required_bytes: int) -> bool:
    return get_free_disk_bytes(destination_root) >= required_bytes
