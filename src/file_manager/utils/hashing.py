from __future__ import annotations

import hashlib
from pathlib import Path


SUPPORTED_HASHES = {"md5", "sha256"}


def hash_file(path: Path, algorithm: str = "sha256", chunk_size: int = 1024 * 1024) -> str:
    algorithm = algorithm.lower()
    if algorithm not in SUPPORTED_HASHES:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")

    hasher = hashlib.new(algorithm)
    with path.open("rb") as file_handle:
        while True:
            chunk = file_handle.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def hash_bytes(content: bytes, algorithm: str = "sha256") -> str:
    algorithm = algorithm.lower()
    if algorithm not in SUPPORTED_HASHES:
        raise ValueError(f"Unsupported hash algorithm: {algorithm}")
    return hashlib.new(algorithm, content).hexdigest()
