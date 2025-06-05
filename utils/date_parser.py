from dateutil.parser import parse as parse_date
from datetime import datetime
from typing import Optional


def parse_natural_date(date_str: str) -> Optional[datetime]:
    try:
        dt = parse_date(date_str, fuzzy=True)
        if dt.date() < datetime.today().date():
            # Reject past dates
            return None
        return dt
    except Exception:
        return None
