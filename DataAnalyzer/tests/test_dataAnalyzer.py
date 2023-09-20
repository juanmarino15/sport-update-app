import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))  # Adds the project root to the Python path.

from unittest.mock import patch
from DataAnalyzer.dataAnalyzer import fetch_tennis_events, country_statistics

class TestDataAnalyzer(unittest.TestCase):

    @patch('DataAnalyzer.dataAnalyzer.retrieve_events')
    def test_fetch_tennis_events(self, mock_retrieve_events):
        mock_data = [
            {
                'event_id': '1234',
                'event_start_time': '2023-09-20T10:00:00Z',
                'competition_name': 'Sample Competition',
                'round_name': 'Sample Round',
                'competitor_1_name': 'Player A',
                'competitor_1_country': 'Colombia',
                'competitor_2_name': 'Player B',
                'competitor_2_country': 'USA',
                'scores': '2-1',
                'flag': 'home'
            }
        ]
        mock_retrieve_events.return_value = mock_data
        events = fetch_tennis_events()
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['competitor_1']['country'], 'Colombia')

    @patch('DataAnalyzer.dataAnalyzer.retrieve_events')
    def test_country_statistics(self, mock_retrieve_events):
        mock_data = [
            {
                'event_id': '1234',
                'event_start_time': '2023-09-20T10:00:00Z',
                'competition_name': 'Sample Competition',
                'round_name': 'Sample Round',
                'competitor_1_name': 'Player A',
                'competitor_1_country': 'Colombia',
                'competitor_2_name': 'Player B',
                'competitor_2_country': 'USA',
                'scores': '2-1',
                'flag': 'Competitors_1_qualifier'
            }
        ]
        mock_retrieve_events.return_value = mock_data
        stats = country_statistics()
        self.assertEqual(stats['Colombia']['players'], 1)
        self.assertEqual(stats['Colombia']['winners'], 1)
        self.assertEqual(stats['USA']['players'], 1)
        self.assertEqual(stats['USA']['winners'], 0)

if __name__ == "__main__":
    unittest.main()
