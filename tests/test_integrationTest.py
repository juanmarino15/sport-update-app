import sys
import os
import unittest
from unittest.mock import patch
import requests
from datetime import datetime, timedelta

# Add the project root to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from webApp import app
from DataAnalyzer.dataAnalyzer import fetch_tennis_events
from DataCollector.apiCollector import structure_data  # Importing structure_data

BASE_URL = 'http://0.0.0.0:5000'

# Mocked event data structure
mock_event = {
    "sport_event": {
        "sport_event_context": {
            "competition": {
                "id": "1234",
                "name": "Sample Competition"
            },
            "round": {
                "name": "Sample Round"
            },
            "season": {
                "id": "5678",
                "name": "Sample Season"
            }
        },
        "start_time": "2023-01-01T10:00:00Z",
        "competitors": [
            {
                "id": "91011",
                "name": "Player A",
                "country": "Country A",
                "country_code": "A",
                "qualifier": "home"
            },
            {
                "id": "121314",
                "name": "Player B",
                "country": "Country B",
                "country_code": "B",
                "qualifier": "away"
            }
        ]
    },
    "sport_event_status": {
        "period_scores": [
            {
                "home_score": 1,
                "away_score": 2
            }
        ],
        "home_score": 1,
        "away_score": 2
    }
}

# Mocked data for the external API
MOCKED_API_RESPONSE = {
    "summaries": [mock_event]
}

# Process the mock_event with structure_data to make it look like the data stored in DB
mock_processed_event = structure_data(mock_event)

# This mock data will be returned when the retrieve_events function from DataAnalyzer is called.
MOCKED_DB_EVENTS = [mock_processed_event]

class WebAppIntegrationTests(unittest.TestCase):

    # @patch('DataAnalyzer.pika.URLParameters')
    @patch('DataAnalyzer.dataAnalyzer.retrieve_events')
    def test_fetch_tennis_events(self, mock_retrieve_events):
        yesterday = datetime.now() - timedelta(1)
        formatted_yesterday = yesterday.strftime('%Y-%m-%d')
        """Test if webApp correctly displays tennis events."""
        response = requests.get(f"http://api.sportradar.us/tennis/trial/v3/en/schedules/{formatted_yesterday}/summaries.json?api_key=uqmpq6cdah4d25ww4wep2znp")

        self.assertEqual(response.status_code, 200)

        # simulating the insertion and retrieval from db
        mock_data = [
            {
                'event_id': '1234',
                'event_start_time': '2023-09-20T10:00:00Z',
                'competition_name': 'Sample Competition',
                'round_name': 'Sample Round',
                'competitor_1_name': 'Player A',
                'competitor_1_country': 'Country A',
                'competitor_2_name': 'Player B',
                'competitor_2_country': 'USA',
                'scores': '2-1',
                'flag': 'home'
            }
        ]

        print(mock_data)

        mock_retrieve_events.return_value = mock_data
        events = fetch_tennis_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['competitor_1']['country'], 'Country A')

    # Check if the mock data's competitors are in the webApp's response
        # for competitor in mock_processed_event["competitors_name"]:
        #     self.assertIn(competitor, response.text)

if __name__ == '__main__':
    unittest.main()
