from __future__ import annotations

import json
import uuid
from collections.abc import Iterable, Iterator
from pathlib import Path

from file_manager.logging.logger import get_logger
from file_manager.models.file_record import FileRecord
from file_manager.scanner.metadata import build_image_record
from file_manager.utils.file_helpers import normalize_extensions
from file_manager.utils.paths import ensure_directory, is_probably_system_path


scan_logger = get_logger("scan")
error_logger = get_logger("errors")

DEFAULT_IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif", ".tiff", ".webp", ".heic"
}


class ImageScanner:
    def __init__(self, compute_hash: bool = False, hash_algorithm: str = "sha256") -> None:
        self.compute_hash = compute_hash
        self.hash_algorithm = hash_algorithm

    def scan(
        self,
        targets: list[Path],
        extensions: list[str] | None = None,
        skip_system_paths: bool = True,
        checkpoint_path: Path | None = None,
    ) -> Iterator[FileRecord]:
        scan_id = str(uuid.uuid4())
        normalized_extensions = normalize_extensions(extensions) or DEFAULT_IMAGE_EXTENSIONS
        processed_paths = self._load_checkpoint(checkpoint_path) if checkpoint_path else set()

        scan_logger.info("Starting image scan %s for targets=%s extensions=%s", scan_id, targets, sorted(normalized_extensions))

        for target in targets:
            if not target.exists():
                error_logger.error("Target does not exist: %s", target)
                continue
            yield from self._scan_target(
                scan_id=scan_id,
                target=target,
                normalized_extensions=normalized_extensions,
                skip_system_paths=skip_system_paths,
                checkpoint_path=checkpoint_path,
                processed_paths=processed_paths,
            )

        scan_logger.info("Completed image scan %s", scan_id)

    def _scan_target(
        self,
        scan_id: str,
        target: Path,
        normalized_extensions: set[str],
        skip_system_paths: bool,
        checkpoint_path: Path | None,
        processed_paths: set[str],
    ) -> Iterable[FileRecord]:
        if target.is_file():
            if self._matches(target, normalized_extensions) and str(target.resolve()) not in processed_paths:
                record = build_image_record(scan_id, target, self.compute_hash, self.hash_algorithm)
                self._mark_progress(checkpoint_path, processed_paths, target)
                yield record
            return

        try:
            for path in target.rglob("*"):
                if skip_system_paths and is_probably_system_path(path):
                    continue
                if not path.is_file():
                    continue
                if not self._matches(path, normalized_extensions):
                    continue
                resolved_text = str(path.resolve())
                if resolved_text in processed_paths:
                    continue
                try:
                    record = build_image_record(scan_id, path, self.compute_hash, self.hash_algorithm)
                    self._mark_progress(checkpoint_path, processed_paths, path)
                    yield record
                except PermissionError:
                    error_logger.warning("Permission denied: %s", path)
                except OSError as exc:
                    error_logger.warning("OS error while scanning %s: %s", path, exc)
                except Exception as exc:  # noqa: BLE001
                    error_logger.exception("Unexpected scan error for %s: %s", path, exc)
        except PermissionError:
            error_logger.warning("Permission denied while entering directory: %s", target)
        except Exception as exc:  # noqa: BLE001
            error_logger.exception("Failed scanning target %s: %s", target, exc)

    @staticmethod
    def _matches(path: Path, normalized_extensions: set[str]) -> bool:
        return path.suffix.lower() in normalized_extensions

    @staticmethod
    def _load_checkpoint(checkpoint_path: Path | None) -> set[str]:
        if checkpoint_path is None or not checkpoint_path.exists():
            return set()
        try:
            payload = json.loads(checkpoint_path.read_text(encoding="utf-8"))
            return set(payload.get("processed_paths", []))
        except Exception:
            return set()

    @staticmethod
    def _mark_progress(checkpoint_path: Path | None, processed_paths: set[str], path: Path) -> None:
        if checkpoint_path is None:
            return
        ensure_directory(checkpoint_path.parent)
        processed_paths.add(str(path.resolve()))
        checkpoint_path.write_text(
            json.dumps({"processed_paths": sorted(processed_paths)}, indent=2),
            encoding="utf-8",
        )
