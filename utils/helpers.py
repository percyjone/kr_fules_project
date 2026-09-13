from datetime import datetime, timedelta

from config.settings import ONLINE_WINDOW_MINUTES


# ==========================================================
# TANK ONLINE / OFFLINE STATUS
# ==========================================================

def row_status(row):

    try:

        ts = datetime.strptime(
            f"{row['date']} {row['time']}",
            "%Y-%m-%d %H:%M:%S"
        )

    except (ValueError, TypeError):

        return "Offline"

    return (
        "Online"
        if datetime.now() - ts
        <= timedelta(minutes=ONLINE_WINDOW_MINUTES)
        else "Offline"
    )