"""Check if LVV relay was on today and send ntfy.sh notification if not."""
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

from get_data_from_shelly_api import fetch_shelly_data

HELSINKI = ZoneInfo("Europe/Helsinki")


def check_lvv():
    api_key = os.environ["SMART_MONITORING_KEY"]
    ntfy_topic = os.environ["NTFY_TOPIC"]
    relay_name = os.environ.get("RELAY_NAME", "LVV")
    notify_always = os.environ.get("NOTIFY_ALWAYS", "").lower() == "true"

    now_helsinki = datetime.now(HELSINKI)
    # Two cron jobs fire daily (18:15 UTC and 19:15 UTC). Only the one landing
    # at hour 21 Helsinki time is the intended run; skip the other.
    if now_helsinki.hour != 21:
        print(f"Not check time (Helsinki {now_helsinki.strftime('%H:%M')}), skipping")
        return

    today = now_helsinki.date()
    print(f"Checking relay '{relay_name}' for date {today} (Helsinki time)")

    df = fetch_shelly_data(api_key)

    lvv = df[df["relenimi"] == relay_name].copy()
    if lvv.empty:
        print(f"WARNING: No data found for relay '{relay_name}'")
        sys.exit(1)

    # Ensure timestamps are timezone-aware UTC, then convert to Helsinki
    if lvv["pvm"].dt.tz is None:
        lvv["pvm"] = lvv["pvm"].dt.tz_localize("UTC")
    lvv["pvm_helsinki"] = lvv["pvm"].dt.tz_convert(HELSINKI)

    lvv_today = lvv[lvv["pvm_helsinki"].dt.date == today]
    was_on = lvv_today["relestatus"].any()

    on_times = lvv_today[lvv_today["relestatus"]]["pvm_helsinki"].tolist()

    if not was_on:
        message = f"{relay_name} not on today! ({today})"
    elif notify_always:
        message = f"OK (debug): {relay_name} was on today at: {[str(t) for t in on_times]}"
    else:
        print(f"OK: {relay_name} was on today at: {[str(t) for t in on_times]}")
        return

    requests.post(
        f"https://ntfy.sh/{ntfy_topic}",
        data=message.encode("utf-8"),
        headers={
            "Title": f"{relay_name} warning" if not was_on else f"{relay_name} OK (debug)",
            "Priority": "high" if not was_on else "default",
            "Tags": "warning" if not was_on else "white_check_mark",
        },
        timeout=10,
    )
    print(f"Notification sent: {message}")
    if not was_on:
        sys.exit(1)


if __name__ == "__main__":
    check_lvv()
