from __future__ import annotations

from pathlib import Path


def discover_labeled_images(dataset_root: Path) -> list[tuple[Path, str]]:
    samples: list[tuple[Path, str]] = []
    for class_dir in dataset_root.iterdir():
        if not class_dir.is_dir():
            continue
        label = class_dir.name
        for file_path in class_dir.rglob("*"):
            if file_path.is_file():
                samples.append((file_path, label))
    return samples
