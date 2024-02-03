import sqlite3



def select_player_for_team(db_name, team_id):
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Write a query to select a player who is not already drafted by any team
    # and meets any other criteria you have (e.g., player level, position, etc.)
    # Note: You might need a more complex query based on your requirements.
    query = """
        SELECT player_id
        FROM dim_players
        WHERE player_id NOT IN (SELECT player_id FROM fact_drafted_players)
        ORDER BY RANDOM()
        LIMIT 1;
    """
    
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result:
        player_id = result[0]
        # Insert the drafted player into the fact_drafted_players table
        cursor.execute("""
            INSERT INTO fact_drafted_players (team_id, player_id)
            VALUES (?, ?);
        """, (team_id, player_id))
        print(f"Team {team_id} drafted Player {player_id}")
        conn.commit()

def draft_players_for_all_teams(db_name):

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Write a query to get a list of all team IDs
    cursor.execute("SELECT team_id FROM dim_teams;")
    team_ids = [row[0] for row in cursor.fetchall()]
    
    # Loop through each team
    for team_id in team_ids:
        # Draft players until the team has 15 players
        while True:
            cursor.execute("""
                SELECT COUNT(*) FROM fact_drafted_players
                WHERE team_id = ?;
            """, (team_id,))
            current_team_size = cursor.fetchone()[0]
            
            if current_team_size >= 15:
                print(f"Team {team_id} has reached 15 players.")
                break
            
            select_player_for_team(db_name, team_id)
    # Close the connection
    conn.close()


def snake_draft_players_for_all_teams(db_name):
    print('Snake Draft is called')
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        print('db connected')

        # Write a query to get a list of all team IDs
        cursor.execute("SELECT team_id FROM dim_teams;")
        team_ids = [row[0] for row in cursor.fetchall()]

        print('Selected all team ids')

        num_players_per_team = 15
        num_rounds = num_players_per_team // len(team_ids)

        print(f"team ids: {team_ids}")

        int(f"num_rounds: {num_rounds}")

        print('round math complete')

        for round_num in range(1, num_rounds + 1):
            print(f"Round {round_num}")
            print('round loop flag')

            # Determine the order in which teams will pick in the current round
            if round_num % 2 == 0:
                draft_order = team_ids[::-1]  # Reverse order for even rounds
            else:
                draft_order = team_ids

                print(f"Draft Order: {draft_order}")

            # Loop through each team in the draft order
            for team_id in draft_order:
                print('team order flag')
                # Draft players until the team has 15 players
                while True:
                    cursor.execute("""
                        SELECT COUNT(*) FROM fact_drafted_players
                        WHERE team_id = ?;
                    """, (team_id,))
                    current_team_size = cursor.fetchone()[0]

                    if current_team_size >= num_players_per_team:
                        print(f"Team {team_id} has reached {num_players_per_team} players.")
                        break

                    select_player_for_team(db_name, team_id)

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()
