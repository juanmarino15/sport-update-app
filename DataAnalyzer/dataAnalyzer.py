#!/usr/bin/env python3

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from database.db import retrieve_events, check_process_status

def fetch_colombian_events():
    # test
    """Fetch today's events where one of the competitors is from Colombia."""

    # Fetch the events from the database
    events = retrieve_events()

    # Store the events
    colombian_events = []
    for event in events:
        colombian_event = {
            "event_id": event['event_id'],
            "start_time": event['event_start_time'],
            "competition": event['competition_name'],
            "round": event['round_name'],
            "competitor_1": {
                "name": event['competitor_1_name'],
                "country": event['competitor_1_country']
            },
            "competitor_2": {
                "name": event['competitor_2_name'],
                "country": event['competitor_2_country']
            },
            "scores": event['scores'],
            "flag": event['flag']
        }
        colombian_events.append(colombian_event)

    return colombian_events

if __name__ == "__main__":

    print("Checking if datacollector has finished processing...")
    while not check_process_status("datacollector"):
        print("Waiting for datacollector to finish...")
        time.sleep(10)

    yesterday = datetime.now() - timedelta(1)
    formatted_yesterday = yesterday.strftime('%Y-%m-%d')
    print(f"Fetching events for {formatted_yesterday} where one of the competitors is from Colombia...")

    colombian_events_today = fetch_colombian_events()
    print(colombian_events_today)
    print(f"Retrieved {len(colombian_events_today)} events from today with Colombian competitors.")
