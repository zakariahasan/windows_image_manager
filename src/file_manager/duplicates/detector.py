from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from file_manager.logging.logger import get_logger
from file_manager.models.duplicate_group import DuplicateGroup
from file_manager.utils.hashing import hash_file


dup_logger = get_logger("duplicates")
error_logger = get_logger("errors")


class DuplicateDetector:
    def __init__(self, algorithm: str = "sha256", chunk_size: int = 1024 * 1024) -> None:
        self.algorithm = algorithm
        self.chunk_size = chunk_size

    def find_duplicates(self, paths: list[Path]) -> list[DuplicateGroup]:
        size_groups: dict[int, list[Path]] = defaultdict(list)
        for path in paths:
            try:
                size_groups[path.stat().st_size].append(path)
            except OSError as exc:
                error_logger.warning("Failed to stat %s: %s", path, exc)

        duplicate_groups: list[DuplicateGroup] = []
        group_counter = 1

        for size_bytes, candidate_paths in size_groups.items():
            if len(candidate_paths) < 2:
                continue

            hash_groups: dict[str, list[Path]] = defaultdict(list)
            for path in candidate_paths:
                try:
                    hash_value = hash_file(path, self.algorithm, self.chunk_size)
                    hash_groups[hash_value].append(path)
                except OSError as exc:
                    error_logger.warning("Failed to hash %s: %s", path, exc)

            for hash_value, files in hash_groups.items():
                if len(files) < 2:
                    continue
                group = DuplicateGroup(
                    group_id=f"dup_{group_counter}",
                    hash_algorithm=self.algorithm,
                    hash_value=hash_value,
                    size_bytes=size_bytes,
                    files=files,
                )
                duplicate_groups.append(group)
                dup_logger.info("Detected duplicate group %s with %s files", group.group_id, len(files))
                group_counter += 1

        return duplicate_groups
