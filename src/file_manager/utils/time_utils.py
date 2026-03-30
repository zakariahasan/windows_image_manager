from __future__ import annotations

from datetime import datetime


def isoformat_from_timestamp(ts: float) -> str:
    return datetime.fromtimestamp(ts).isoformat(timespec="seconds")
