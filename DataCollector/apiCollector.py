#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from datetime import datetime, timedelta
from database.db import check_event_id_exists, insert_event
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


# Calculate the date for today - 1
yesterday = datetime.now() - timedelta(1)
formatted_yesterday = yesterday.strftime('%Y-%m-%d')
print(formatted_yesterday)

# Fetching the data from the API
url = f"http://api.sportradar.us/tennis/trial/v3/en/schedules/{formatted_yesterday}/summaries.json?api_key=uqmpq6cdah4d25ww4wep2znp"
response = requests.get(url)
data = response.json()
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

# Filter and structure the data based on the given requirements
# Apply our structure function
structured_data = [structure_data(event) for event in data["summaries"]]
print(structured_data)

# Insert the data into the database
for event in structured_data:
    if not check_event_id_exists(event["event_id"]):  # check for each event
        insert_event(event)
        print('data inserted')
print('Data insertion done')
