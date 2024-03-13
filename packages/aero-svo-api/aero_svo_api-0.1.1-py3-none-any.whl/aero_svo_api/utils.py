from datetime import datetime


def format_date(date: datetime) -> str:
    return date.isoformat(timespec='seconds').replace('+', '%2B')
