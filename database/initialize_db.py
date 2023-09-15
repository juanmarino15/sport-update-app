import os
import psycopg2

def initialize_db():
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL)
    print('connected to db')

    cur = conn.cursor()

    commands = (
        """
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
        );
        """
    )

    # Execute the commands
    for command in commands:
        cur.execute(command)

    # Commit the changes and close the connection
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    initialize_db()
