import requests

# Fetching the data from the API
url = "http://api.sportradar.us/tennis/trial/v3/en/schedules/2023-09-10/summaries.json?api_key=uqmpq6cdah4d25ww4wep2znp"
response = requests.get(url)
data = response.json()

# Filter and structure the data based on the given requirements
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
        "date": event["sport_event"]["start_time"].split("T")[0],
        "competition_name": event["sport_event"]["sport_event_context"]["competition"]["name"],
        "round_name": event["sport_event"]["sport_event_context"]["round"]["name"],
        "competitors_name": [c["name"] for c in competitors],
        "competitors_country": [c.get("country", "N/A") for c in competitors],
        "competitors_country_code": [c.get("country_code", "N/A") for c in competitors],
        "competitors_qualifier": [c["qualifier"] for c in competitors],
        "scores": scores_format,
        "flag": flag
    }

    return structured

# Apply our structure function
structured_data = [structure_data(event) for event in data["summaries"]]

print(structured_data)
