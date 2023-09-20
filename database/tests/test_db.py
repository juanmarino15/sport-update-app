import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))  # Adds the project root to the Python path.

from database.db import get_db_connection, insert_event, check_event_id_exists, retrieve_events

class TestDBFunctions(unittest.TestCase):

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
        insert_event(self.event)

    def tearDown(self):
        # This method will run after every test method
        # Cleanup: Delete the event inserted for testing
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sport_events WHERE event_id = %s", (self.event['event_id'],))
        conn.commit()
        cursor.close()
        conn.close()

    def test_insert_event(self):
        # Verify the event is inserted
        self.assertTrue(check_event_id_exists('12345'))

    def test_retrieve_events(self):
        events = retrieve_events()
        self.assertTrue(any(event['event_id'] == '12345' for event in events))

    # Add more tests for other functions...

if __name__ == '__main__':
    unittest.main()
