from __future__ import annotations

from pathlib import Path

from PIL import Image, UnidentifiedImageError

from file_manager.models.file_record import FileRecord
from file_manager.utils.file_helpers import guess_mime_type
from file_manager.utils.hashing import hash_file
from file_manager.utils.time_utils import isoformat_from_timestamp


def build_image_record(scan_id: str, path: Path, compute_hash: bool = False, hash_algorithm: str = "sha256") -> FileRecord:
    stat = path.stat()
    size_bytes = stat.st_size
    width = None
    height = None
    image_format = None
    image_mode = None
    is_valid_image = False
    remarks = None

    try:
        with Image.open(path) as img:
            width, height = img.size
            image_format = img.format
            image_mode = img.mode
            is_valid_image = True
    except (UnidentifiedImageError, OSError) as exc:
        remarks = f"invalid-image: {exc}"

    record = FileRecord(
        scan_id=scan_id,
        file_name=path.name,
        full_path=path.resolve(),
        extension=path.suffix.lower(),
        size_bytes=size_bytes,
        size_mb=round(size_bytes / (1024 * 1024), 4),
        created_at=isoformat_from_timestamp(stat.st_ctime),
        modified_at=isoformat_from_timestamp(stat.st_mtime),
        accessed_at=isoformat_from_timestamp(stat.st_atime),
        mime_type=guess_mime_type(path),
        width=width,
        height=height,
        image_format=image_format,
        image_mode=image_mode,
        is_valid_image=is_valid_image,
        remarks=remarks,
    )
    if compute_hash:
        record.hash_algorithm = hash_algorithm
        record.hash_value = hash_file(path, algorithm=hash_algorithm)
    return record
