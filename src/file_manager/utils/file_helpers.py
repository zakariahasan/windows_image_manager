from __future__ import annotations

import mimetypes
from pathlib import Path


def guess_mime_type(path: Path) -> str | None:
    mime, _ = mimetypes.guess_type(path.name)
    return mime


def normalize_extensions(extensions: list[str] | None) -> set[str] | None:
    if not extensions:
        return None
    normalized = set()
    for ext in extensions:
        ext = ext.strip().lower()
        if not ext:
            continue
        if not ext.startswith("."):
            ext = f".{ext}"
        normalized.add(ext)
    return normalized or None
