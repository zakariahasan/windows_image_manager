from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image


def extract_image_features(path: Path, size: tuple[int, int] = (128, 128)) -> np.ndarray:
    with Image.open(path) as img:
        img = img.convert("RGB")
        img = img.resize(size)
        array = np.asarray(img, dtype=np.float32) / 255.0
        mean_rgb = array.mean(axis=(0, 1))
        std_rgb = array.std(axis=(0, 1))
        flattened_small = np.asarray(img.resize((32, 32)), dtype=np.float32).flatten() / 255.0
        return np.concatenate([mean_rgb, std_rgb, flattened_small])
