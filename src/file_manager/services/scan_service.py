from __future__ import annotations

from pathlib import Path

from file_manager.scanner.scanner import ImageScanner
from file_manager.utils.csv_utils import export_records_to_csv


class ScanService:
    def run_scan(
        self,
        targets: list[Path],
        output_csv: Path,
        extensions: list[str] | None = None,
        compute_hash: bool = False,
        checkpoint_path: Path | None = None,
    ) -> int:
        scanner = ImageScanner(compute_hash=compute_hash)
        records = list(scanner.scan(targets, extensions, checkpoint_path=checkpoint_path))
        export_records_to_csv(records, output_csv)
        return len(records)
