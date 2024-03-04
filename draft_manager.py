import sqlite3
import random


#Initial draft functions-------------------------------------
def select_random_player_for_team(db_name, team_id):
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
        #print(f"Team {team_id} drafted Player {player_id}")
        conn.commit()

def select_best_position_player_for_team(db_name, team_id, round_num, num_players_per_team, salary_cap):
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    try:
        round_num = int(round_num)
        num_players_per_team = int(num_players_per_team)
    except ValueError as e:
        raise ValueError(f"Error: {e}")


    # Calculate the remaining salary budget for the team
    cursor.execute("""
        SELECT SUM(dim_players.player_salary)
        FROM fact_drafted_players
        LEFT JOIN dim_players ON dim_players.player_id = fact_drafted_players.player_id
        WHERE fact_drafted_players.team_id = ?;
    """, (team_id,))
    result = cursor.fetchone()

    total_salary_used = result[0]

   
    
    if not isinstance(result[0], int):
        total_salary_used = 0
    else:
        total_salary_used = result[0]

    #total_salary_used = "0" if isinstance(result, type(None)) else result[0]
    
    try:
        total_salary_used = int(total_salary_used)
    except ValueError:
        raise ValueError("Error: total_salary_used is not a valid integer.")

    remaining_salary_budget = salary_cap - (num_players_per_team - round_num) - total_salary_used

    # Determine if the team needs to fulfill position requirements
    #print(f"Remaining Salary Budget: {remaining_salary_budget}")

   
    
    # Calculate the positional needs for the team
    cursor.execute("""
        SELECT positions.position,
                COALESCE(players_by_position.player_count, 0) as player_count
                FROM
                    (
                        SELECT 'Point Guard' AS position
                        UNION SELECT 'Shooting Guard'
                        UNION SELECT 'Small Forward'
                        UNION SELECT 'Power Forward'
                        UNION SELECT 'Center'
	                ) AS positions
                LEFT JOIN (
                        SELECT dim_players.position, 
		                count(*) as player_count
                        FROM fact_drafted_players
                        INNER JOIN dim_players ON dim_players.player_id = fact_drafted_players.player_id
                        WHERE team_id = ?
	                    GROUP BY 1
                          ) AS players_by_position ON positions.position = players_by_position.position
                        ORDER BY player_count ASC
                    """, (team_id,))

    result = cursor.fetchall()

    # print("Query output:")
    # for row in result:
    #     print(row)



    # if result:
    #     selected_position = result[0]
    #     if not isinstance(result[1], int):
    #         position_count = 0
    #     else:
    #         position_count = result[1]
    # else:
    #     positions = ['Point Guard', 'Shooting Guard', 'Small Forward', 'Power Forward', 'Center']
    #     selected_position = random.choice(positions)
    #     position_count = 0

    lowest_positions = []

    for position, player_count in result:
        lowest_count = result[0][1]
        if player_count <= lowest_count:
            lowest_count = player_count
            lowest_positions.append(position)

        # elif player_count == lowest_count:
        #     lowest_positions.append(position)

    # Randomly select one of the positions with the lowest count
    selected_position = random.choice(lowest_positions)

    
    if lowest_count < 2:
        # The team needs to fulfill position requirements
        #print("Fulfilling Position Requirements")
        

        query = """
            SELECT player_id
            FROM dim_players
            WHERE player_id NOT IN (SELECT player_id FROM fact_drafted_players)
                AND position = ?
                AND player_salary <= ?
            ORDER BY overall_score DESC
            LIMIT 1;
        """

        cursor.execute(query, (selected_position, remaining_salary_budget))
    else:
        # The team doesn't have position requirements
        #print("No Position Requirements")
        query = """
            SELECT player_id
            FROM dim_players
            WHERE player_id NOT IN (SELECT player_id FROM fact_drafted_players)
                AND player_salary <= ?
            ORDER BY overall_score DESC
            LIMIT 1;
        """

        cursor.execute(query, (remaining_salary_budget,))

    result = cursor.fetchone()

    
    if result:
        player_id = result[0]
        # Insert the drafted player into the fact_drafted_players table
        cursor.execute("""
            INSERT INTO fact_drafted_players (team_id, player_id)
            VALUES (?, ?);
        """, (team_id, player_id))
        #print(f"Team {team_id} drafted Player {player_id}")
        conn.commit()


def full_team_draft_players_for_all_teams(db_name):

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
                #print(f"Team {team_id} has reached 15 players.")
                break
            
            select_random_player_for_team(db_name, team_id)
    # Close the connection
    conn.close()


def snake_draft_players_for_all_teams(db_name, salary_cap):
    #print('Snake Draft is called')
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        #print('db connected')

        # Write a query to get a list of all team IDs
        cursor.execute("SELECT team_id FROM dim_teams;")
        team_ids = [row[0] for row in cursor.fetchall()]

        #print('Selected all team ids')

        num_players_per_team = 15
        #num_rounds = num_players_per_team // len(team_ids)
        num_rounds = num_players_per_team

        #print(f"team ids: {team_ids}")

        #int(f"num_rounds: {num_rounds}")

        #print('round math complete')

        for round_num in range(1, num_rounds + 1):
            print(f"Round {round_num}")
            #print('round loop flag')

            # Determine the order in which teams will pick in the current round
            if round_num % 2 == 0:
                draft_order = team_ids[::-1]  # Reverse order for even rounds
                print(f"Draft Order: {draft_order}")
            else:
                draft_order = team_ids

                print(f"Draft Order: {draft_order}")

            # Loop through each team in the draft order
            for team_id in draft_order:
                #Select one player per team
                select_best_position_player_for_team(db_name, team_id, round_num, num_players_per_team, salary_cap)
                #select_random_player_for_team(db_name, team_id)


    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        # Close the connection
        if conn:
            conn.close()
