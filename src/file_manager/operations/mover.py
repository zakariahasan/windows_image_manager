from __future__ import annotations

import shutil
from pathlib import Path

from file_manager.logging.logger import get_logger
from file_manager.operations.duplicate_policy import DuplicateHandling, resolve_destination
from file_manager.utils.disk import has_enough_disk_space
from file_manager.utils.paths import ensure_directory


app_logger = get_logger("app")
error_logger = get_logger("errors")


def move_file(source: Path, destination_dir: Path, policy: DuplicateHandling, dry_run: bool = False) -> tuple[bool, str, Path | None]:
    ensure_directory(destination_dir)
    if not has_enough_disk_space(destination_dir, source.stat().st_size):
        return False, "insufficient-disk-space", None

    desired_destination = destination_dir / source.name
    resolved, status = resolve_destination(source, desired_destination, policy)
    if resolved is None:
        app_logger.info("Move skipped for %s due to policy status=%s", source, status)
        return True, status, None

    if dry_run:
        app_logger.info("Dry run move %s -> %s", source, resolved)
        return True, f"dry-run-{status}", resolved

    try:
        shutil.move(str(source), str(resolved))
        app_logger.info("Moved %s -> %s", source, resolved)
        return True, status, resolved
    except Exception as exc:  # noqa: BLE001
        error_logger.exception("Move failed %s -> %s: %s", source, resolved, exc)
        return False, str(exc), None
