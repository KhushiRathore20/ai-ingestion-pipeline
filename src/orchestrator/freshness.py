from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime


def parse_date(value):
    if not value:
        return None

    value = value.strip()

    # ISO-8601
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt.astimezone(timezone.utc)

    except ValueError:
        pass

    # RFC email/RSS dates
    try:
        dt = parsedate_to_datetime(value)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt.astimezone(timezone.utc)

    except (TypeError, ValueError):
        return None


def is_fresh(value, hours=24):
    published = parse_date(value)

    if published is None:
        return False

    now = datetime.now(timezone.utc)

    age = now - published

    return timedelta(0) <= age <= timedelta(hours=hours)


def deduplicate(records, key="source_url"):
    seen = set()
    unique = []

    for record in records:
        value = record.get(key)

        if not value or value in seen:
            continue

        seen.add(value)
        unique.append(record)

    return unique