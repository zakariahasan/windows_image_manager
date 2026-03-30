from __future__ import annotations

from file_manager.operations.duplicate_policy import DuplicateHandling, resolve_destination


def test_duplicate_policy_skip(temp_files) -> None:
    resolved, status = resolve_destination(temp_files["a"], temp_files["b"], DuplicateHandling.SKIP)
    assert resolved is None
    assert status == "skipped-existing"
