#Create views to hold team rosters to be used for game simulator logic
import sqlite3

def create_team_roster(db_name, team_id):
    """
    Creates a view for a specific team's roster based on their team_id.

    Parameters:
        db_name (str): The SQLite database file name.
        team_id (int): The ID of the team to create a view for.
    """
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Define the view name
    view_name = f"team_{team_id}_roster"

    # SQL query to create the view
    sql = f"""
    DROP VIEW IF EXISTS {view_name} AS
    SELECT  
        p.player_id,  
        p.first_name,  
        p.last_name,  
        p.position,  
        p.overall_rating,  
        p.height,  
        p.weight,  
        p.birth_year,  
        d.contract_years,  
        d.salary  
    FROM fact_drafted_players d  
    JOIN dim_players p ON d.player_id = p.player_id  
    WHERE d.team_id = ?;
    """

    # Execute the query using parameterized SQL to prevent injection
    cursor.execute(sql, (team_id,))

    # Commit changes and close connection
    conn.commit()
    conn.close()

    print(f"View for team {team_id} created successfully.")



    
