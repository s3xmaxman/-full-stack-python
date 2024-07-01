from datetime import datetime, timezone


def get_utc_datetime() -> datetime:
    return datetime.now(timezone.utc)
