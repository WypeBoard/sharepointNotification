from datetime import datetime, date


def __now() -> datetime:
    return datetime.now()


def get_datetime() -> datetime:
    return __now()


def get_date() -> date:
    return __now().date()


def from_database_datetime(date_time_str: str) -> datetime:
    if date_time_str is None:
        raise RuntimeError
    return datetime.fromisoformat(date_time_str).replace(microsecond=0)

