import unittest
import sys
import os
import psycopg2

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
                event_id text PRIMARY KEY,
                event_start_time timestamp,
                competition_name text,
                round_name text,
                competitor_1_name text,
                competitor_1_country text,
                competitors_1_qualifier text,
                competitor_2_name text,
                competitor_2_country text,
                competitors_2_qualifier text,
                scores text,
                flag text
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
        # This method will run before every test method
        self.event = {
            'event_id': '12345',
            'date': '2023-09-20',
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
