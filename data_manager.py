import sqlite3
#Only imported for testing
import player_generator
import team_generator


#Create tables functions-------------------
#dim_players
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

#dim_teams
def create_team_table(db_name, teams):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table (example table: dim_teams)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dim_teams (
            team_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            ) VALUES (NULL, ?, ?)
        ''', (
            team.location_name, team.team_name, 
        ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

#fact_drafted_players
def create_draft_table(db_name, draft):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table (example table: fact_drafted_players)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fact_drafted_players (
            draft_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            team_id INTEGER,
            draft_order INTEGER,
            FOREIGN KEY (player_id) REFERENCES dim_players(player_id),
            FOREIGN KEY (team_id) REFERENCES dim_teams(team_id)
        )
    ''')

    # Commit the changes
    conn.commit()

    # Assume you have the 'teams' list with team objects

    #teams = team_generator.generate_teams(30)

    # Insert data from the 'roster' list
    for drafted_players in draft:
        cursor.execute('''
            INSERT INTO fact_drafter_players (
                draft_id, player_id, team_id, draft_order
            ) VALUES (NULL, ?, ?, ?)
        ''', (
            draft.player_id, draft.team_id, draft.draft_order, 
        ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

#fact_team_rosters
def create_team_roster_table(db_name, team_roster):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table (example table: dim_team)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fact_team_rosters (
            roster_id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            team_id INTEGER,
            FOREIGN KEY (player_id) REFERENCES dim_players(player_id),
            FOREIGN KEY (team_id) REFERENCES dim_teams(team_id)
        )
    ''')

    # Commit the changes
    conn.commit()

    # Assume you have the 'teams' list with team objects

    #teams = team_generator.generate_teams(30)

    # Insert data from the 'roster' list
    for players in team_roster:
        cursor.execute('''
            INSERT INTO fact_team_rosters (
                roster_id, player_id, team_id
            ) VALUES (NULL, ?, ?)
        ''', (
            team_roster.player_id, team_roster.team_id 
        ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

#Print tables functions---------------------

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

    cursor.execute('SELECT * FROM dim_teams')
    
    # Fetch all the rows
    rows = cursor.fetchall()

    # Print the results
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

#Drop tables/ data mangement functions----------
def drop_table(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

    # Commit the changes
    conn.commit()


#For testing
#roster = player_generator.generate_roster(80, 'rookies') 
#create_player_table("league01.db", roster)
#print_player_table("league01.db")
drop_table("league01.db", "dim_teams")
teams = team_generator.generate_teams(30)
create_team_table("league01.db", teams)    
print_team_table("league01.db") 

#drop_table("league01.db", "dim_teams")