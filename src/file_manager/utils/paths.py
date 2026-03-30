from __future__ import annotations

from pathlib import Path


WINDOWS_SYSTEM_DIR_NAMES = {
    "$Recycle.Bin",
    "System Volume Information",
    "Windows",
}


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def is_probably_system_path(path: Path) -> bool:
    return any(part in WINDOWS_SYSTEM_DIR_NAMES for part in path.parts)


def unique_destination_path(destination: Path) -> Path:
    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    parent = destination.parent
    counter = 1

    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1
