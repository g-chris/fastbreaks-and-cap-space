#Create fact tables for individual player and game results
import sqlite3

def create_fact_game_results(db_name):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table (example table: dim_teams)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fact_game_results (
    game_id INTEGER PRIMARY KEY,
    season_id INTEGER,
    game_day INTEGER,
    home_team_id INTEGER,
    away_team_id INTEGER,
    home_score INTEGER,
    away_score INTEGER,
    winner_team_id INTEGER,
    losing_team_id INTEGER,
    ot_count INTEGER,
    FOREIGN KEY (home_team_id) REFERENCES dim_teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES dim_teams(team_id)
);
    ''')

    # Commit the changes
    conn.commit()

def record_game_results(db_name, game_id, season_id, game_day,
                        home_team_id, away_team_id, home_score, away_score, winner_team_id, losing_team_id, ot_count):
     
      # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()


    cursor.execute('''
            INSERT INTO fact_game_results (
                game_id, season_id, game_day, home_team_id, away_team_id, home_score, away_score, winner_team_id, losing_team_id, ot_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            game_id, season_id, game_day, home_team_id, away_team_id, home_score, away_score, winner_team_id, losing_team_id, ot_count
        ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

