#!/usr/bin/env python3

import sys
import os
import time
from collections import OrderedDict
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timedelta
from database.db import retrieve_events, check_process_status

def fetch_tennis_events(country = None):
    # test
    """Fetch today's events where one of the competitors is from Colombia."""
    if not country:
        country = "Colombia"


    # Fetch the events from the database
    events = retrieve_events(country)

    # Store the events
    country_events = []
    for event in events:
        country_event = {
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
        country_events.append(country_event)


    return country_events

def country_statistics():
    events = retrieve_events()

    # Dictionary to store player counts and winners count per country
    stats = {}

    for event in events:
        # Check for competitor_1
        c1_country = event['competitor_1_country']
        if c1_country not in stats:
            stats[c1_country] = {'players': 0, 'winners': 0}
        stats[c1_country]['players'] += 1

        # Check for competitor_2
        c2_country = event['competitor_2_country']
        if c2_country not in stats:
            stats[c2_country] = {'players': 0, 'winners': 0}
        stats[c2_country]['players'] += 1

        # Check winner
        if event['flag'] == "Competitors_1_qualifier":
            stats[c1_country]['winners'] += 1
        else:
            stats[c2_country]['winners'] += 1

    sorted_stats = OrderedDict(sorted(stats.items()))
    return sorted_stats


if __name__ == "__main__":

    print("Checking if datacollector has finished processing...")

    # queue simulation. If the datacollector is still collecting data, we wait on queue until is done. once its done the rest of the code runs
    while not check_process_status("datacollector"):
        print("Waiting for datacollector to finish...")
        time.sleep(10)

    country_events_today = fetch_tennis_events()
    print(country_events_today)
    print(f"Retrieved {len(country_events_today)} events from today with Colombian competitors.")

    # Call the statistics function and print results
    stats = country_statistics()
    print(stats) #stast
    for country, data in stats.items():
        print(f"{country}: Players - {data['players']}, Winners - {data['winners']}")