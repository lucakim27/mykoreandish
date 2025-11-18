from datetime import datetime
import pytz

def format_time_ago(timestamp):
    utc = pytz.UTC
    now = datetime.now(utc)
    timestamp_aware = timestamp.astimezone(utc)
    delta = now - timestamp_aware
    if delta.days > 0:
        return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
    elif delta.seconds // 3600 > 0:
        hours = delta.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif delta.seconds // 60 > 0:
        minutes = delta.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "just now"
