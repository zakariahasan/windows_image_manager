from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class LogSettings:
    log_dir: Path = Path("logs")
    log_level: str = "INFO"
    max_bytes: int = 5 * 1024 * 1024
    backup_count: int = 5


@dataclass(slots=True)
class ScanSettings:
    chunk_size: int = 1024 * 1024
    follow_symlinks: bool = False
    compute_hash_on_scan: bool = False
    default_hash_algorithm: str = "sha256"


@dataclass(slots=True)
class TransferSettings:
    buffer_size: int = 65536
    timeout_seconds: int = 30
    bind_host: str = "0.0.0.0"
    default_port: int = 50505


@dataclass(slots=True)
class ArchiveSettings:
    compression_level: int = 6
    default_archive_dir: Path = Path("output") / "archives"


@dataclass(slots=True)
class MlSettings:
    model_dir: Path = Path("models")
    image_size: tuple[int, int] = (128, 128)
    test_size: float = 0.2
    random_state: int = 42


@dataclass(slots=True)
class AppSettings:
    output_dir: Path = Path("output")
    temp_dir: Path = Path("temp")
    dry_run: bool = False
    log: LogSettings = field(default_factory=LogSettings)
    scan: ScanSettings = field(default_factory=ScanSettings)
    transfer: TransferSettings = field(default_factory=TransferSettings)
    archive: ArchiveSettings = field(default_factory=ArchiveSettings)
    ml: MlSettings = field(default_factory=MlSettings)
