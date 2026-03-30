from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(slots=True)
class FileRecord:
    scan_id: str
    file_name: str
    full_path: Path
    extension: str
    size_bytes: int
    size_mb: float
    created_at: str
    modified_at: str
    accessed_at: str
    mime_type: str | None = None
    width: int | None = None
    height: int | None = None
    image_format: str | None = None
    image_mode: str | None = None
    is_valid_image: bool | None = None
    hash_algorithm: str | None = None
    hash_value: str | None = None
    duplicate_group_id: str | None = None
    action_taken: str | None = None
    action_status: str | None = None
    remarks: str | None = None

    def to_csv_row(self) -> dict[str, object]:
        row = asdict(self)
        row["full_path"] = str(self.full_path)
        return row
