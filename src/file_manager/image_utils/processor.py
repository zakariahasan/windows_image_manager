from __future__ import annotations

from pathlib import Path

from PIL import Image

from file_manager.utils.paths import ensure_directory


def resize_image(path: Path, output_path: Path, size: tuple[int, int]) -> Path:
    ensure_directory(output_path.parent)
    with Image.open(path) as img:
        resized = img.resize(size)
        resized.save(output_path)
    return output_path


def convert_image(path: Path, output_path: Path, target_format: str) -> Path:
    ensure_directory(output_path.parent)
    with Image.open(path) as img:
        rgb_img = img.convert("RGB")
        rgb_img.save(output_path, format=target_format.upper())
    return output_path


def create_thumbnail(path: Path, output_path: Path, size: tuple[int, int] = (128, 128)) -> Path:
    ensure_directory(output_path.parent)
    with Image.open(path) as img:
        img.thumbnail(size)
        img.save(output_path)
    return output_path
