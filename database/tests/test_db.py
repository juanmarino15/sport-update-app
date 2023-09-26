import unittest
import sys
import os
import psycopg2
from datetime import datetime,timedelta


sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))  # Adds the project root to the Python path.

from database.db import insert_event, check_event_id_exists, retrieve_events

class TestDBFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # This method will run once before all test methods
        # Establish a database connection for testing
        cls.conn = psycopg2.connect(
            dbname="sportsUpdate",
            user="sportsUpdate",
            password="sportsUpdate",
            host="localhost",  # Assuming the PostgreSQL container is running locally
            port="5432"
        )
        # Create the sport_events table if it doesn't exist
        cursor = cls.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sport_events (
                event_id TEXT PRIMARY KEY,
                event_start_time TIMESTAMP,
                sport_name TEXT,
                category_name TEXT,
                competition_name TEXT,
                season_name TEXT,
                stage_type TEXT,
                stage_phase TEXT,
                round_name TEXT,
                best_of INT,
                competitor_1_name TEXT,
                competitor_1_country TEXT,
                competitors_1_qualifier TEXT,
                competitor_2_name TEXT,
                competitor_2_country TEXT,
                competitors_2_qualifier TEXT,
                venue_name TEXT,
                venue_city TEXT,
                venue_country TEXT,
                event_status TEXT,
                match_status TEXT,
                home_score INT,
                away_score INT,
                winner_id TEXT,
                scores TEXT,
                flag TEXT
            )
        """)
        cls.conn.commit()
        cursor.close()

    @classmethod
    def tearDownClass(cls):
        # This method will run once after all test methods
        # Close the database connection after all tests
        cls.conn.close()

    def setUp(self):
        yesterday = datetime.now() - timedelta(1)
        formatted_yesterday = yesterday.strftime('%Y-%m-%d')
        # This method will run before every test method
        self.event = {
            'event_id': '12345',
            'date': formatted_yesterday,
            'competition_name': 'Test Competition',
            'round_name': 'Final',
            'competitors_name': ['A', 'B'],
            'competitors_country': ['USA', 'UK'],
            'competitors_qualifier': ['Qualifier1', 'Qualifier2'],
            'scores': '5-5',
            'flag': 'Some flag'
        }
        # Insert event
        insert_event(self.event, self.conn)

    def tearDown(self):
        # This method will run after every test method
        # Cleanup: Delete the event inserted for testing
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM sport_events WHERE event_id = %s", (self.event['event_id'],))
        self.conn.commit()
        cursor.close()

    def test_insert_event(self):
        # Verify the event is inserted
        self.assertTrue(check_event_id_exists('12345', self.conn))

    def test_retrieve_events(self,):
        events = retrieve_events('USA',self.conn)
        self.assertTrue(any(event['event_id'] == '12345' for event in events))

    # Add more tests for other functions...

if __name__ == '__main__':
    unittest.main()
