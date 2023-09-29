import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))  # Adds the project root to the Python path.

from unittest.mock import patch
from webApp.app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    @patch('DataAnalyzer.dataAnalyzer.fetch_tennis_events')
    @patch('DataAnalyzer.dataAnalyzer.country_statistics')
    def test_main_route(self, mock_country_stats, mock_tennis_events):
        mock_tennis_events.return_value = []
        mock_country_stats.return_value = {}

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tennis Events Results', response.data)

    @patch('DataAnalyzer.dataAnalyzer.fetch_tennis_events')   # Adjust the path if needed
    @patch('DataAnalyzer.dataAnalyzer.country_statistics')    # Adjust the path if needed
    def test_post_country(self, mock_country_stats, mock_tennis_events):
        mock_tennis_events.return_value = []
        mock_country_stats.return_value = {}

        response = self.client.post('/', data={'country': 'USA'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No results found for tennis players from USA', response.data)

if __name__ == '__main__':
    unittest.main()
