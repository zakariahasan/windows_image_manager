from __future__ import annotations

import socket
from pathlib import Path

from file_manager.logging.logger import get_logger
from file_manager.transfer.protocol import build_header


transfer_logger = get_logger("transfer")


def send_file(host: str, port: int, path: Path, buffer_size: int = 65536) -> None:
    with socket.create_connection((host, port), timeout=30) as sock:
        sock.sendall(build_header(path))
        with path.open("rb") as file_handle:
            while True:
                chunk = file_handle.read(buffer_size)
                if not chunk:
                    break
                sock.sendall(chunk)
    transfer_logger.info("Sent file %s to %s:%s", path, host, port)
