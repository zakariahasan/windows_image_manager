from __future__ import annotations

from pathlib import Path

from file_manager.archive.zipper import create_zip_archive


class ArchiveService:
    def create(self, paths: list[Path], archive_path: Path, password: str | None = None) -> Path:
        return create_zip_archive(paths, archive_path, password)
