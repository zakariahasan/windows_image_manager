from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def temp_files(tmp_path: Path) -> dict[str, Path]:
    file_a = tmp_path / "a.txt"
    file_b = tmp_path / "b.txt"
    file_c = tmp_path / "c.txt"

    file_a.write_text("same-content", encoding="utf-8")
    file_b.write_text("same-content", encoding="utf-8")
    file_c.write_text("different-content", encoding="utf-8")

    return {"a": file_a, "b": file_b, "c": file_c, "root": tmp_path}
