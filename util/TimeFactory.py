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


def get_gui_date() -> str:
    return get_date().strftime('%d-%m-%Y')


def get_gui_datetime() -> str:
    return get_datetime().strftime('%d-%m-%Y %T')


def to_gui_date(date_time: datetime = get_datetime()) -> str:
    return date_time.strftime('%d-%m-%Y')
