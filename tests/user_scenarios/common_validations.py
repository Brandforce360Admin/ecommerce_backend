from datetime import datetime
from uuid import UUID


def is_valid_uuid(val):
    try:
        UUID(str(val))
        return True
    except ValueError:
        return False


def is_valid_datetime(dt_str):
    try:
        datetime.fromisoformat(dt_str)
    except:
        return False
    return True
