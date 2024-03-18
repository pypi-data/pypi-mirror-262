from __future__ import annotations

import pendulum

TZ_UTC = pendulum.UTC


def get_posix_timestamp() -> float:
    """The current POSIX time as a float."""
    return pendulum.now(TZ_UTC).timestamp()


def datetime_from_timestamp(timestamp: float) -> pendulum.DateTime:
    """Convert a float POSIX time to a datetime object in UTC."""
    return pendulum.from_timestamp(timestamp)
