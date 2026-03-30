from __future__ import annotations

from pathlib import Path

from PIL import Image, UnidentifiedImageError


def is_valid_image(path: Path) -> bool:
    try:
        with Image.open(path) as img:
            img.verify()
        return True
    except (UnidentifiedImageError, OSError):
        return False


def get_image_info(path: Path) -> dict[str, object]:
    with Image.open(path) as img:
        return {
            "format": img.format,
            "mode": img.mode,
            "size": img.size,
            "width": img.width,
            "height": img.height,
        }


def read_exif(path: Path) -> dict[str, object]:
    with Image.open(path) as img:
        exif = img.getexif()
        return {str(tag): value for tag, value in exif.items()}
