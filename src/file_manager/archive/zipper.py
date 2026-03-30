from __future__ import annotations

import zipfile
from pathlib import Path

from file_manager.logging.logger import get_logger
from file_manager.utils.paths import ensure_directory

archive_logger = get_logger("archive")
error_logger = get_logger("errors")

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tif", ".tiff", ".webp", ".heic"
}


def create_zip_archive(
    paths: list[Path],
    archive_path: Path,
    password: str | None = None,
    compression_level: int = 6,
    images_only: bool = False,
) -> Path:
    ensure_directory(archive_path.parent)
    archive_logger.info(
        "Starting archive creation archive=%s password_enabled=%s images_only=%s",
        archive_path,
        bool(password),
        images_only,
    )

    files_to_add = list(_iter_files(paths, images_only=images_only))
    archive_logger.info("Resolved %s file(s) to add into archive %s", len(files_to_add), archive_path)

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
                for file_path, arcname in files_to_add:
                    archive_logger.info("Adding file to protected archive source=%s arcname=%s", file_path, arcname)
                    zf.write(file_path, arcname=str(arcname))
            archive_logger.info("Created password-protected archive at %s", archive_path)
            return archive_path
        except ImportError:
            archive_logger.warning(
                "pyzipper not installed, falling back to standard zip without password protection"
            )

    with zipfile.ZipFile(
        archive_path,
        "w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=compression_level,
    ) as zf:
        for file_path, arcname in files_to_add:
            archive_logger.info("Adding file to archive source=%s arcname=%s", file_path, arcname)
            zf.write(file_path, arcname=str(arcname))

    archive_logger.info("Created archive at %s", archive_path)
    return archive_path


def _iter_files(paths: list[Path], images_only: bool = False):
    for source in paths:
        source = Path(source)

        if not source.exists():
            error_logger.warning("Archive source does not exist: %s", source)
            continue

        if source.is_file():
            if images_only and source.suffix.lower() not in IMAGE_EXTENSIONS:
                archive_logger.info("Skipping non-image file during archive build: %s", source)
                continue
            yield source, source.name
            continue

        if source.is_dir():
            for file_path in source.rglob("*"):
                if not file_path.is_file():
                    continue
                if images_only and file_path.suffix.lower() not in IMAGE_EXTENSIONS:
                    continue
                arcname = file_path.relative_to(source.parent)
                yield file_path, arcname
