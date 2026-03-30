from __future__ import annotations

from pathlib import Path

from PIL import Image
import imagehash


def perceptual_hash(path: Path) -> str:
    with Image.open(path) as img:
        return str(imagehash.phash(img))
