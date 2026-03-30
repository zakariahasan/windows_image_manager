from __future__ import annotations

from file_manager.scanner.scanner import FileScanner


def test_scanner_filters_extension(temp_files) -> None:
    scanner = FileScanner()
    records = list(scanner.scan([temp_files["root"]], extensions=[".txt"]))
    assert len(records) == 3
