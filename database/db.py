import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        dbname="sportsUpdate",
        user="sportsUpdate",
        password="sportsUpdate",
        host="postgres",
        port="5432"
    )
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
            competitor_2_name, 
            competitor_2_country,
            competitors_1_qualifier,
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
