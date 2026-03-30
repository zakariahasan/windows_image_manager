from __future__ import annotations

import zipfile
from pathlib import Path

from file_manager.logging.logger import get_logger
from file_manager.utils.paths import ensure_directory


archive_logger = get_logger("archive")
error_logger = get_logger("errors")


def create_zip_archive(
    paths: list[Path],
    archive_path: Path,
    password: str | None = None,
    compression_level: int = 6,
) -> Path:
    ensure_directory(archive_path.parent)

    if password:
        try:
            import pyzipper

            with pyzipper.AESZipFile(
                archive_path,
                "w",
                compression=zipfile.ZIP_DEFLATED,
                compresslevel=compression_level,
                encryption=pyzipper.WZ_AES,
            ) as zf:
                zf.setpassword(password.encode("utf-8"))
                for path in paths:
                    if path.is_file():
                        zf.write(path, arcname=path.name)
            archive_logger.info("Created password-protected archive at %s", archive_path)
            return archive_path
        except ImportError:
            archive_logger.warning("pyzipper not installed, falling back to standard zip without password")

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zf:
        for path in paths:
            if path.is_file():
                zf.write(path, arcname=path.name)
    archive_logger.info("Created archive at %s", archive_path)
    return archive_path
