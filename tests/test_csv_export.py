from __future__ import annotations

from file_manager.scanner.scanner import FileScanner
from file_manager.utils.csv_utils import export_records_to_csv


def test_csv_export_creates_file(temp_files) -> None:
    scanner = FileScanner()
    records = list(scanner.scan([temp_files["root"]], extensions=[".txt"]))
    csv_path = temp_files["root"] / "out.csv"
    export_records_to_csv(records, csv_path)
    assert csv_path.exists()
