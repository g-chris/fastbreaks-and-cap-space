import sqlite3
import player_generator
import team_generator

def create_player_table(db_name, roster):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table (example table: dim_players)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dim_players (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    #Commented out for production, let's pass in the roster elsewhere so we can handle the initial draft and subsequent rookie classes

    #roster = player_generator.generate_roster(400, 'normal')

    # Insert data from the 'roster' list
    for player in roster:
        cursor.execute('''
            INSERT INTO dim_players (
                player_id, first_name, last_name, position, player_level,
                overall_score, player_salary,
                attribute_strength, attribute_dexterity, attribute_constitution,
                attribute_intelligence, attribute_shooting, attribute_defense
            ) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

def create_team_table(db_name, teams):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table (example table: dim_team)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dim_team (
            team_id INTEGER PRIMARY KEY,
            location_name TEXT,
            team_name TEXT
        )
    ''')

    # Commit the changes
    conn.commit()

    # Assume you have the 'teams' list with team objects

    #teams = team_generator.generate_teams(30)

    # Insert data from the 'roster' list
    for team in teams:
        cursor.execute('''
            INSERT INTO dim_team (
                team_id, location_name, team_name
            ) VALUES (?, ?, ?)
        ''', (
            team.team_id, team.location_name, team.team_name, 
        ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def print_player_table(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM dim_players ORDER BY player_id')
    
    # Fetch all the rows
    rows = cursor.fetchall()

    # Print the results
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

def print_team_table(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM dim_team')
    
    # Fetch all the rows
    rows = cursor.fetchall()

    # Print the results
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

def drop_table(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

    # Commit the changes
    conn.commit()


#For testing
#roster = player_generator.generate_roster(80, 'rookies') 
#create_player_table("league01.db", roster)
print_player_table("league01.db")
#create_team_table()    
#print_team_table() 

#drop_table("league01.db", "dim_players")