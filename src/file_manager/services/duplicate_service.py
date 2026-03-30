from __future__ import annotations

from pathlib import Path

from file_manager.duplicates.detector import DuplicateDetector


class DuplicateService:
    def find(self, paths: list[Path]) -> list:
        detector = DuplicateDetector()
        return detector.find_duplicates(paths)
