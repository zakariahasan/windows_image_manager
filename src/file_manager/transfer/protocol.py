from __future__ import annotations

import json
from pathlib import Path

from file_manager.models.transfer_models import TransferHeader
from file_manager.utils.hashing import hash_file


def build_header(path: Path) -> bytes:
    header = TransferHeader(
        file_name=path.name,
        file_size=path.stat().st_size,
        checksum=hash_file(path),
    )
    payload = json.dumps(header.__dict__).encode("utf-8")
    return len(payload).to_bytes(8, "big") + payload


def parse_header(raw: bytes) -> TransferHeader:
    data = json.loads(raw.decode("utf-8"))
    return TransferHeader(**data)
