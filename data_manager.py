import sqlite3
import player_generator

def create_player_table():
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

    # Commit the changes
    conn.commit()

    # Assume you have the 'roster' list with player objects

    roster = player_generator.generate_roster(400, 'normal')

    # Insert data from the 'roster' list
    for player in roster:
        cursor.execute('''
            INSERT INTO players (
                first_name, last_name, position, player_level,
                overall_score, player_salary,
                attribute_strength, attribute_dexterity, attribute_constitution,
                attribute_intelligence, attribute_shooting, attribute_defense
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            player.first_name, player.last_name, player.position, player.player_level,
            player.overall_score, player.player_salary,
            player.attributes['strength'], player.attributes['dexterity'],
            player.attributes['constitution'], player.attributes['intelligence'],
            player.attributes['shooting'], player.attributes['defense']
        ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def print_player_table():
    conn = sqlite3.connect('league01.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM players ORDER BY overall_score DESC')
    
    # Fetch all the rows
    rows = cursor.fetchall()

    # Print the results
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

print_player_table()