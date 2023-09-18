#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from datetime import datetime, timedelta
from database.db import check_event_id_exists, insert_event, set_process_status
import uuid
import re


# Helper functions
def extract_number_from_id(string_id):
    match = re.search(r'(\d+)', string_id)
    if match:
        return match.group(1)
    return ''

def get_custom_event_id(event):
    # Extracting required IDs
    competition_id = extract_number_from_id(event["sport_event"]["sport_event_context"]["competition"]["id"])
    season_id = extract_number_from_id(event["sport_event"]["sport_event_context"]["season"]["id"])
    competitor_1_id = extract_number_from_id(event["sport_event"]["competitors"][0]["id"])
    competitor_2_id = extract_number_from_id(event["sport_event"]["competitors"][1]["id"])

    # Concatenating extracted numbers to form event_ID
    return competition_id + season_id + competitor_1_id + competitor_2_id
def structure_data(event):
    competitors = event["sport_event"]["competitors"]
    # Check if "period_scores" exists
    scores = event["sport_event_status"].get("period_scores", [])

    # Mapping scores
    scores_list = []
    for score in scores:
        score_string = f"{score['home_score']} - {score['away_score']}"
        scores_list.append(score_string)
    scores_format = ", ".join(scores_list)

    # Check if "home_score" and "away_score" exist
    home_total_score = event["sport_event_status"].get("home_score", 0)
    away_total_score = event["sport_event_status"].get("away_score", 0)

    flag = "home" if home_total_score > away_total_score else "away"

    structured = {
        "event_id": get_custom_event_id(event),
        "date": event["sport_event"].get("start_time", "N/A").split("T")[0],
        "competition_name": event["sport_event"]["sport_event_context"]["competition"].get("name", "N/A"),
        "round_name": event["sport_event"]["sport_event_context"]["round"].get("name", "N/A"),
        "competitors_name": [c.get("name", "N/A") for c in competitors],
        "competitors_country": [c.get("country", "N/A") for c in competitors],
        "competitors_country_code": [c.get("country_code", "N/A") for c in competitors],
        "competitors_qualifier": [c.get("qualifier", "N/A") for c in competitors],
        "scores": scores_format,
        "flag": flag
    }

    return structured






def main():
    set_process_status("datacollector", True)

    # Calculate the date for yesterday
    yesterday = datetime.now() - timedelta(1)
    formatted_yesterday = yesterday.strftime('%Y-%m-%d')
    print(formatted_yesterday)

    # Fetch data from the API
    url = f"http://api.sportradar.us/tennis/trial/v3/en/schedules/{formatted_yesterday}/summaries.json?api_key=uqmpq6cdah4d25ww4wep2znp"

    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code.
        data = response.json()

        # Filter and structure the data
        structured_data = [structure_data(event) for event in data["summaries"]]

        # Insert the data into the database
        for event in structured_data:
            if not check_event_id_exists(event["event_id"]):  # Check for each event
                insert_event(event)
                print('Data inserted')

        print('Data insertion done')

    except requests.RequestException as e:
        print(f"Error fetching data from the API: {e}")

    finally:
        set_process_status("datacollector", False)

if __name__ == "__main__":
    main()
