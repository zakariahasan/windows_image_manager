from __future__ import annotations

import shutil
from pathlib import Path

from file_manager.image_utils.inspector import get_image_info, is_valid_image
from file_manager.utils.paths import ensure_directory


def organize_images_by_format(source_dir: Path, destination_root: Path) -> None:
    ensure_directory(destination_root)
    for path in source_dir.rglob("*"):
        if not path.is_file():
            continue
        if not is_valid_image(path):
            continue
        info = get_image_info(path)
        target_dir = ensure_directory(destination_root / str(info["format"]).lower())
        shutil.copy2(path, target_dir / path.name)
