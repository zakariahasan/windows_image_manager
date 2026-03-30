from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from file_manager.models.file_record import FileRecord
from file_manager.utils.paths import ensure_directory


CSV_FIELDS = [
    "scan_id",
    "file_name",
    "full_path",
    "extension",
    "size_bytes",
    "size_mb",
    "created_at",
    "modified_at",
    "accessed_at",
    "mime_type",
    "width",
    "height",
    "image_format",
    "image_mode",
    "is_valid_image",
    "hash_algorithm",
    "hash_value",
    "duplicate_group_id",
    "action_taken",
    "action_status",
    "remarks",
]


def export_records_to_csv(records: Iterable[FileRecord], output_path: Path) -> Path:
    ensure_directory(output_path.parent)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        for record in records:
            writer.writerow(record.to_csv_row())
    return output_path


def read_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


def write_csv_rows(rows: list[dict[str, object]], output_path: Path) -> Path:
    ensure_directory(output_path.parent)
    fieldnames = list(rows[0].keys()) if rows else CSV_FIELDS
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return output_path
