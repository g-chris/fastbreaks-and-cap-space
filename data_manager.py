import sqlite3


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
                player_id, first_name, nick_name, last_name, position, player_level,
                overall_score, player_salary,
                attribute_strength, attribute_dexterity, attribute_constitution,
                attribute_intelligence, attribute_shooting, attribute_defense
            ) VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            player.first_name, player.nick_name, player.last_name, player.position, player.player_level,
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
            team_name TEXT,
            conf_div_id INTEGER,
            FOREIGN KEY (conf_div_id) REFERENCES fact_conferences_divisions(conf_div_id)
        )
    ''')

    # Commit the changes
    conn.commit()

    # Assume you have the 'teams' list with team objects

    #teams = team_generator.generate_teams(30)

    # Insert data from the 'roster' list
    for team in teams:
        cursor.execute('''
            INSERT INTO dim_teams (
                team_id, location_name, team_name, conf_div_id
            ) VALUES (NULL, ?, ?, ?)
        ''', (
            team.location_name, team.team_name, team.conf_div_id
        ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

#fact_conferences_divisions
def create_conferences_and_divsions_table(db_name, conferences_and_divisions):
     # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table (example table: dim_teams)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fact_conferences_divisions (
            conf_div_id INTEGER PRIMARY KEY AUTOINCREMENT,
            conference_name TEXT,
            division_name TEXT
        )
    ''')

    # Commit the changes
    conn.commit()

    for pairs in conferences_and_divisions:
        cursor.execute('''
            INSERT INTO fact_conferences_divisions (
                conf_div_id, conference_name, division_name
            ) VALUES (NULL, ?, ?)
        ''', (
            pairs[0], pairs[1]
        ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

#fact_drafted_players
def create_draft_table(db_name):
    
    #print('create_draft_table called')
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Check if the table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='fact_drafted_players'")
    table_exists = cursor.fetchone()

    if not table_exists:
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

    # Close the connection
    conn.close()

    #draft_manager will handle loading
    """ # Insert data from the 'roster' list
    for drafted_players in draft:
        cursor.execute('''
            INSERT INTO fact_drafted_players (
                draft_id, player_id, team_id, draft_order
            ) VALUES (NULL, ?, ?, ?)
        ''', (
            draft.player_id, draft.team_id, draft.draft_order, 
        ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close() """

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

#fact_season_schedule
def create_season_schedule (db_name, season_num, schedule):
    conn = sqlite3.connect(db_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fact_season_schedule (
            game_id INTEGER PRIMARY KEY AUTOINCREMENT,
            season_id INTEGER,
            game_day INTEGER,
            home_team_id INTEGER,
            away_team_id INTEGER,
            FOREIGN KEY (home_team_id) REFERENCES dim_teams(team_id),
            FOREIGN KEY (away_team_id) REFERENCES dim_teams(team_id)
        )
    ''')

    # Commit the changes
    conn.commit()

    for game_set in schedule:
        home_team = game_set[0]
        away_team = game_set[1]
        game_day = game_set[2]
        
        cursor.execute('''
        INSERT INTO fact_season_schedule (
            game_id, 
            season_id, 
            game_day,
            home_team_id,
            away_team_id
        ) VALUES (NULL, ?, ?, ?, ?)
        ''', (season_num, game_day, home_team, away_team ))

       
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

#dim_roster_positions
def create_dim_roster_positions(db_name):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table (example table: dim_teams)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dim_roster_positions (
            roster_position_id INTEGER PRIMARY KEY AUTOINCREMENT,
            position_name TEXT,
            team_name TEXT,
            conf_div_id INTEGER,
            FOREIGN KEY (conf_div_id) REFERENCES fact_conferences_divisions(conf_div_id)
        )
    ''')

    # Commit the changes
    conn.commit()

    # Assume you have the 'teams' list with team objects

    #teams = team_generator.generate_teams(30)

    # Insert data from the 'roster' list
    for team in teams:
        cursor.execute('''
            INSERT INTO dim_teams (
                team_id, location_name, team_name, conf_div_id
            ) VALUES (NULL, ?, ?, ?)
        ''', (
            team.location_name, team.team_name, team.conf_div_id
        ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


#Print tables functions---------------------
#For testing/debugging only

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

def print_draft_table(db_name):
    try:
        conn = sqlite3.connect(db_name)
        #print('Connected to the database')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM fact_drafted_players')
        
        # Fetch all the rows
        rows = cursor.fetchall()

        # Print the results
        for row in rows:
            print(row)

        # Close the connection
        conn.close()
        #print('Closed the connection')
    except Exception as e:
        print(f"An error occurred: {e}")

#Drop tables/ data mangement functions----------
def drop_table(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

    # Commit the changes
    conn.commit()

    
