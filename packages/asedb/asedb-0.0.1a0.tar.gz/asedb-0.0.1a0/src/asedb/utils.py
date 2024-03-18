from __future__ import annotations

from typing import Any


def float_or_none(value: Any) -> float | None:
    if value is None:
        return None
    return float(value)
