import sqlite3
import game_sim_engine

def create_team_roster_view(conn, team_id):
    cursor = conn.cursor()
    view_name = f"team_{team_id}_roster"
    
    # Drop the view if it exists
    cursor.execute(f"DROP VIEW IF EXISTS {view_name}")
    
    # Create a new view from dim_player_transactions
    cursor.execute(f"""
        CREATE VIEW {view_name} AS
        SELECT
            p.player_id,
            p.first_name,
            p.last_name,
            p.position,
            p.overall_score
        FROM dim_player_transactions t
        JOIN dim_players p ON t.player_id = p.player_id
        WHERE t.team_id = {team_id} AND t.etl_current_flag = 1
    """)
    conn.commit()

def simulate_game(game_id, game_day, home_team_id, away_team_id, conn):
    cursor = conn.cursor()

    # Get team names from dim_teams
    cursor.execute("SELECT location_name, team_name FROM dim_teams WHERE team_id = ?", (home_team_id,))
    home_team = cursor.fetchone()
    cursor.execute("SELECT location_name, team_name FROM dim_teams WHERE team_id = ?", (away_team_id,))
    away_team = cursor.fetchone()

    home_team_name = f"{home_team[0]} {home_team[1]}"
    away_team_name = f"{away_team[0]} {away_team[1]}"

    home_score, away_score = game_sim_engine.game_sim(home_team_id, away_team_id, conn)

    print(f"Day {game_day} | Game {game_id}: {away_team_name} {away_score} @ {home_team_name} {home_score}")


def run_season_schedule(db_name, current_season):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Pull the full season schedule for the current season
    cursor.execute("""
        SELECT game_id, game_day, home_team_id, away_team_id
        FROM fact_season_schedule
        WHERE season_id = ?
        ORDER BY game_day, game_id
    """, (current_season,))

    games = cursor.fetchall()

    for game in games:
        game_id, game_day, home_team_id, away_team_id = game

        # Create up-to-date views for both teams
        create_team_roster_view(conn, home_team_id)
        create_team_roster_view(conn, away_team_id)

        # Simulate the game
        simulate_game(game_id, game_day, home_team_id, away_team_id, conn)

    conn.close()
