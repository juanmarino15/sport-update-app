import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))  # Adds the project root to the Python path.
from DataCollector.apiCollector import extract_number_from_id, get_custom_event_id, structure_data


class TestDataCollector(unittest.TestCase):

    def test_extract_number_from_id(self):
        self.assertEqual(extract_number_from_id("sr:match:12345"), "12345")
        self.assertEqual(extract_number_from_id("12345abc"), "12345")
        self.assertEqual(extract_number_from_id("abc"), "")

    def test_get_custom_event_id(self):
        mock_event = {
            "sport_event": {
                "sport_event_context": {
                    "competition": {
                        "id": "comp-1234",
                        "name": "Sample Competition"
                    },
                    "season": {
                        "id": "season-5678",
                        "name": "Sample Season"
                    }
                },
                "competitors": [
                    {
                        "id": "player-91011",
                        "name": "Player A",
                        "country": "Country A",
                        "country_code": "A",
                        "qualifier": "home"
                    },
                    {
                        "id": "player-121314",
                        "name": "Player B",
                        "country": "Country B",
                        "country_code": "B",
                        "qualifier": "away"
                    }
                ]
            }
        }
        expected_event_id = "1234567891011121314"
        self.assertEqual(get_custom_event_id(mock_event), expected_event_id)

    def test_structure_data(self):
        mock_event = {
            "sport_event": {
                "sport_event_context": {
                    "competition": {
                        "id": "comp-1234",
                        "name": "Sample Competition"
                    },
                    "round": {
                        "name": "Sample Round"
                    },
                    "season": {
                        "id": "season-5678",
                        "name": "Sample Season"
                    }
                },
                "start_time": "2023-01-01T10:00:00Z",
                "competitors": [
                    {
                        "id": "player-91011",
                        "name": "Player A",
                        "country": "Country A",
                        "country_code": "A",
                        "qualifier": "home"
                    },
                    {
                        "id": "player-121314",
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

        structured_result = structure_data(mock_event)
        self.assertEqual(structured_result["date"], "2023-01-01")
        self.assertEqual(structured_result["competition_name"], "Sample Competition")
        self.assertEqual(structured_result["round_name"], "Sample Round")
        self.assertEqual(structured_result["competitors_name"], ["Player A", "Player B"])
        self.assertEqual(structured_result["competitors_country"], ["Country A", "Country B"])
        self.assertEqual(structured_result["scores"], "1 - 2")
        self.assertEqual(structured_result["flag"], "away")

if __name__ == '__main__':
    unittest.main()
