from __future__ import annotations

from pathlib import Path

from file_manager.transfer.receiver import receive_once
from file_manager.transfer.sender import send_file


class TransferService:
    def send(self, host: str, port: int, path: Path) -> None:
        send_file(host, port, path)

    def receive(self, bind_host: str, port: int, destination_dir: Path) -> Path:
        return receive_once(bind_host, port, destination_dir)
