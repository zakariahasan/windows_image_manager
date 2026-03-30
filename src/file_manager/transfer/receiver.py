from __future__ import annotations

import socket
from pathlib import Path

from file_manager.logging.logger import get_logger
from file_manager.transfer.protocol import parse_header
from file_manager.utils.hashing import hash_file
from file_manager.utils.paths import ensure_directory, unique_destination_path


transfer_logger = get_logger("transfer")
error_logger = get_logger("errors")


def receive_once(bind_host: str, port: int, destination_dir: Path, buffer_size: int = 65536) -> Path:
    ensure_directory(destination_dir)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((bind_host, port))
        server.listen(1)
        transfer_logger.info("Receiver listening on %s:%s", bind_host, port)
        conn, address = server.accept()
        with conn:
            transfer_logger.info("Connection accepted from %s", address)
            header_len = int.from_bytes(_recv_exact(conn, 8), "big")
            header = parse_header(_recv_exact(conn, header_len))

            output_path = unique_destination_path(destination_dir / header.file_name)
            remaining = header.file_size
            with output_path.open("wb") as file_handle:
                while remaining > 0:
                    chunk = conn.recv(min(buffer_size, remaining))
                    if not chunk:
                        break
                    file_handle.write(chunk)
                    remaining -= len(chunk)

            actual_checksum = hash_file(output_path)
            if actual_checksum != header.checksum:
                error_logger.error("Checksum mismatch for %s", output_path)
                raise ValueError("Checksum verification failed")

            transfer_logger.info("Received file %s", output_path)
            return output_path


def _recv_exact(conn: socket.socket, size: int) -> bytes:
    data = b""
    while len(data) < size:
        chunk = conn.recv(size - len(data))
        if not chunk:
            raise ConnectionError("Connection closed before receiving expected bytes")
        data += chunk
    return data
