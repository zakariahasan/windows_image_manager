from __future__ import annotations

from pathlib import Path

from file_manager.operations.copier import copy_file
from file_manager.operations.duplicate_policy import DuplicateHandling
from file_manager.operations.mover import move_file


class FileActionService:
    def copy_many(self, sources: list[Path], destination_dir: Path, policy: DuplicateHandling, dry_run: bool = False) -> list[tuple[bool, str, Path | None]]:
        return [copy_file(source, destination_dir, policy, dry_run) for source in sources]

    def move_many(self, sources: list[Path], destination_dir: Path, policy: DuplicateHandling, dry_run: bool = False) -> list[tuple[bool, str, Path | None]]:
        return [move_file(source, destination_dir, policy, dry_run) for source in sources]
