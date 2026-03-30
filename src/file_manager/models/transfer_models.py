from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class TransferHeader:
    file_name: str
    file_size: int
    checksum: str


@dataclass(slots=True)
class TransferResult:
    source: Path
    destination: Path
    success: bool
    checksum_verified: bool
    message: str
