from __future__ import annotations

from pathlib import Path

import joblib

from file_manager.utils.paths import ensure_directory


def save_artifact(obj: object, path: Path) -> Path:
    ensure_directory(path.parent)
    joblib.dump(obj, path)
    return path


def load_artifact(path: Path) -> object:
    return joblib.load(path)
