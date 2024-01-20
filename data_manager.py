import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('league01.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table (example table: dim_players)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        player_id INTEGER PRIMARY KEY,
        first_name TEXT,
        nick_name TEXT,
        last_name TEXT,
        position TEXT,
        player_level TEXT,
        overall_score INTEGER,
        player_salary INTEGER,
        attribute_strength INTEGER,
        attribute_dexterity INTEGER,
        attribute_constitution INTEGER,
        attribute_intelligence INTEGER,
        attribute_shooting INTEGER,
        attribute_defense INTEGER
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
