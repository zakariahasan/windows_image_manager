from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar


T = TypeVar("T")


def retry_call(func: Callable[[], T], retries: int = 3, delay_seconds: float = 0.5) -> T:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            return func()
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt == retries:
                break
            time.sleep(delay_seconds)
    assert last_error is not None
    raise last_error
