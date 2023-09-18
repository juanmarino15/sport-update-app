import psycopg2
import os

def get_db_connection():
    # conn = psycopg2.connect(
    #     dbname="sportsUpdate",
    #     user="sportsUpdate",
    #     password="sportsUpdate",
    #     host="postgres",
    #     port="5432"
    # )
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL)
    return conn
# test
def check_event_id_exists(event_id):
    """Check if an event with the given ID already exists."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sport_events WHERE event_id = %s", (event_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def insert_event(event):
    print(event['date'])
    print(event['competitors_country'])

    if not check_event_id_exists(event['event_id']):
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO sport_events (
            event_id,
            event_start_time, 
            competition_name, 
            round_name, 
            competitor_1_name, 
            competitor_1_country, 
            competitors_1_qualifier,
            competitor_2_name, 
            competitor_2_country,
            competitors_2_qualifier,
            scores,
            flag
        ) VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)
        """

        values = (
            event['event_id'],
            event['date'],
            event['competition_name'],
            event['round_name'],
            event['competitors_name'][0] if len(event['competitors_name']) > 0 else None,
            event['competitors_country'][0] if len(event['competitors_country']) > 0 else None,
            event['competitors_qualifier'][0] if len(event['competitors_qualifier']) > 0 else None,
            event['competitors_name'][1] if len(event['competitors_name']) > 1 else None,
            event['competitors_country'][1] if len(event['competitors_country']) > 1 else None,
            event['competitors_qualifier'][1] if len(event['competitors_qualifier']) > 1 else None,
            event['scores'],
            event['flag'],
        )

        cursor.execute(query, values)
        conn.commit()

        cursor.close()
        conn.close()
    else:
        print(f"Event with ID {event['event_id']} already exists in the database.")

from datetime import datetime,timedelta

def retrieve_events(country):
    # Fetch today's date
    yesterday = datetime.now() - timedelta(1)
    formatted_yesterday = yesterday.strftime('%Y-%m-%d')
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT * 
        FROM sport_events 
        WHERE event_start_time = %s 
        AND (competitor_1_country = %s OR competitor_2_country = %s)
    """
    cursor.execute(query, (formatted_yesterday, country, country))
    cursor.execute(query, (formatted_yesterday,))

    results = cursor.fetchall()
    conn.close()

    # Convert results into a list of dictionaries
    events = [{
        "event_id": row[0],
        "event_start_time": row[1],
        "competition_name": row[4],
        "round_name": row[8],
        "competitor_1_name": row[10],
        "competitor_1_country": row[11],
        "competitors_1_qualifier": row[12],
        "competitor_2_name": row[13],
        "competitor_2_country": row[14],
        "competitors_2_qualifier": row[15],
        "scores": row[24],
        "flag": row[25]
    } for row in results]

    return events

def set_process_status(process_name, status):
    """Set the status of a process in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if process_name already exists
    cursor.execute("SELECT COUNT(*) FROM process_status WHERE process_name = %s", (process_name,))
    count = cursor.fetchone()[0]

    if count == 0:
        # If process_name doesn't exist, insert a new record
        cursor.execute(
            "INSERT INTO process_status (process_name, is_completed) VALUES (%s, %s)",
            (process_name, status)
        )
    else:
        # If process_name exists, update the status
        cursor.execute(
            "UPDATE process_status SET is_completed = %s WHERE process_name = %s",
            (status, process_name)
        )

    conn.commit()
    cursor.close()
    conn.close()

def check_process_status(process_name):
    """Check the status of a process in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT is_completed FROM process_status WHERE process_name = %s",
        (process_name,)
    )
    status = cursor.fetchone()
    cursor.close()
    conn.close()

    if status:
        return status[0]
    else:
        return None


