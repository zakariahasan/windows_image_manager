from __future__ import annotations

from file_manager.utils.hashing import hash_file


def test_same_content_has_same_hash(temp_files) -> None:
    assert hash_file(temp_files["a"]) == hash_file(temp_files["b"])


def test_different_content_has_different_hash(temp_files) -> None:
    assert hash_file(temp_files["a"]) != hash_file(temp_files["c"])
