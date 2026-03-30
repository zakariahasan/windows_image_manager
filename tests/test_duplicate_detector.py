from __future__ import annotations

from file_manager.duplicates.detector import DuplicateDetector


def test_duplicate_detector_finds_group(temp_files) -> None:
    detector = DuplicateDetector()
    groups = detector.find_duplicates([temp_files["a"], temp_files["b"], temp_files["c"]])
    assert len(groups) == 1
    assert len(groups[0].files) == 2
