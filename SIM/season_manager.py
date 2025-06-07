import sqlite3
import SIM.game_sim_engine as game_sim_engine
import DATABASE.game_data_manager as game_data_manager

def create_standings_view(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    view_name = "conference_standings"
    
    # Drop the view if it exists
    cursor.execute(f"DROP VIEW IF EXISTS {view_name}")
    
    # Create a new view from dim_player_transactions
    cursor.execute(f"""
                CREATE VIEW {view_name} AS
SELECT 
    results.year,
    results.team_id,
    ROW_NUMBER() OVER (
        PARTITION BY results.conference_name, results.year 
        ORDER BY results.wins DESC, results.win_diff DESC
    ) AS conference_standing,
    results.conference_name,
    results.location_name,
    results.team_name,
    results.wins,
    results.losses,
    results.win_diff
FROM (
    SELECT 
        t.team_id,
        fgr.season_id AS year,
        t.location_name,
        t.team_name,
        c.conference_name,
        c.division_name,
        SUM(CASE WHEN fgr.winner_team_id = t.team_id THEN 1 ELSE 0 END) AS wins,
        SUM(CASE WHEN fgr.losing_team_id = t.team_id THEN 1 ELSE 0 END) AS losses,
        SUM(
            CASE 
                WHEN fgr.winner_team_id = t.team_id THEN 
                    CASE WHEN fgr.home_score > fgr.away_score THEN fgr.home_score - fgr.away_score
                         ELSE fgr.away_score - fgr.home_score
                    END
                ELSE 0
            END
        ) AS win_diff
    FROM dim_teams t
    JOIN dim_conferences_divisions c ON t.conf_div_id = c.conf_div_id
    LEFT JOIN fact_game_results fgr ON (
        fgr.winner_team_id = t.team_id OR fgr.losing_team_id = t.team_id
    )
    WHERE fgr.game_day != 'null'
    GROUP BY t.team_id, year, t.location_name, t.team_name, c.conference_name, c.division_name
) AS results
ORDER BY results.year DESC, results.conference_name DESC, conference_standing;
    """)
    conn.commit()


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

def simulate_game(game_id, game_day, home_team_id, away_team_id, db_name, current_season):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Get team names from dim_teams
    cursor.execute("SELECT location_name, team_name FROM dim_teams WHERE team_id = ?", (home_team_id,))
    home_team = cursor.fetchone()
    cursor.execute("SELECT location_name, team_name FROM dim_teams WHERE team_id = ?", (away_team_id,))
    away_team = cursor.fetchone()

    home_team_name = f"{home_team[0]} {home_team[1]}"
    away_team_name = f"{away_team[0]} {away_team[1]}"

    home_score, away_score, ot_count = game_sim_engine.game_sim(home_team_id, away_team_id, conn)

    if home_score > away_score:
        winner_team_id = home_team_id
        losing_team_id = away_team_id
    else:
        winner_team_id = away_team_id
        losing_team_id = home_team_id

    
    game_data_manager.record_game_results(db_name, game_id, current_season, game_day, home_team_id, away_team_id,
                                          home_score, away_score, winner_team_id, losing_team_id, ot_count)

    # if ot_count == 0:
    #     print(f"Day {game_day} | Game {game_id}: {away_team_name} {away_score} @ {home_team_name} {home_score}")
    # else:
    #     print(f"Day {game_day} | Game {game_id}: {away_team_name} {away_score} @ {home_team_name} {home_score} OT:{ot_count}")


    return winner_team_id

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
        simulate_game(game_id, game_day, home_team_id, away_team_id, db_name, current_season)

    conn.close()

def run_playoff_series(db_name, high_seed_id, low_seed_id, current_season):

    high_seed_wins = 0
    low_seed_wins = 0
    high_seed_homecourt = [0,1,4,6]

    # while high_seed_wins < 4 and low_seed_wins < 4:
    #     game_id = int(str(current_season) + str(high_seed_id) + str('00')+str(low_seed_id) + str(high_seed_wins+low_seed_wins+1))
    #     game_day = 'null'
    #     if high_seed_wins + low_seed_wins in high_seed_homecourt:
    #         game_winner_id = simulate_game(game_id, game_day,high_seed_id, low_seed_id, db_name, current_season)
    #         if game_winner_id == high_seed_id:
    #             high_seed_wins = high_seed_wins + 1
    #         else:
    #             low_seed_wins = low_seed_wins + 1
    #     else:
    #         game_winner_id = simulate_game(game_id, game_day,low_seed_id, high_seed_id, db_name, current_season)
    #         if game_winner_id == high_seed_id:
    #             high_seed_wins = high_seed_wins + 1
    #         else:
    #             low_seed_wins = low_seed_wins + 1

    while high_seed_wins < 4 and low_seed_wins < 4:
        game_number = high_seed_wins + low_seed_wins + 1
        game_id = int(f"{current_season}1{high_seed_id:02d}{low_seed_id:02d}{game_number}")
        game_day = 'null'

        # Determine home/away
        if high_seed_wins + low_seed_wins in high_seed_homecourt:
            home_team_id = high_seed_id
            away_team_id = low_seed_id
        else:
            home_team_id = low_seed_id
            away_team_id = high_seed_id

        # Simulate game and update series state
        game_winner_id = simulate_game(game_id, game_day, home_team_id, away_team_id, db_name, current_season)

        if game_winner_id == high_seed_id:
            high_seed_wins += 1
        else:
            low_seed_wins += 1

    if high_seed_wins > low_seed_wins:
        series_winning_team_id = high_seed_id
    else:
        series_winning_team_id = low_seed_id

    return series_winning_team_id

def playoff_bracket(db_name, current_season):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Fetch all rows from the view, ordered by year, conference, and standing
    cursor.execute(f"""
    SELECT year, conference_standing, team_id
    FROM conference_standings
    WHERE year = {current_season}
    ORDER BY year, conference_name, conference_standing
    """)
    rows = cursor.fetchall()

    # Flatten list of tuples to a simple list
    team_ids = [row[2] for row in rows]

    # Split and take top 8 from each conference
    conference1_top8 = team_ids[:8]
    conference2_top8 = team_ids[15:23]

    #print("Top 8 from Conference 1:", conference1_top8)
    #print("Top 8 from Conference 2:", conference2_top8)

    conn.close()

    return conference1_top8, conference2_top8

def run_post_season(db_name, current_season):
    
    conference1, conference2 = playoff_bracket(db_name,current_season)
    
    #Round 1
    winner_conf1_1_8_seed = run_playoff_series(db_name, conference1[0], conference1[7], current_season)
    winner_conf1_2_7_seed = run_playoff_series(db_name, conference1[1], conference1[6], current_season)
    winner_conf1_3_6_seed = run_playoff_series(db_name, conference1[2], conference1[5], current_season)
    winner_conf1_4_5_seed = run_playoff_series(db_name, conference1[3], conference1[4], current_season)

    winner_conf2_1_8_seed = run_playoff_series(db_name, conference2[0], conference2[7], current_season)
    winner_conf2_2_7_seed = run_playoff_series(db_name, conference2[1], conference2[6], current_season)
    winner_conf2_3_6_seed = run_playoff_series(db_name, conference2[2], conference2[5], current_season)
    winner_conf2_4_5_seed = run_playoff_series(db_name, conference2[3], conference2[4], current_season)


    #Round 2
    winner_conf1_top_bracket = run_playoff_series(db_name, winner_conf1_1_8_seed, winner_conf1_4_5_seed, current_season)
    winner_conf1_bottom_bracket = run_playoff_series(db_name, winner_conf1_2_7_seed, winner_conf1_3_6_seed , current_season)

    winner_conf2_top_bracket = run_playoff_series(db_name, winner_conf2_1_8_seed, winner_conf2_4_5_seed, current_season)
    winner_conf2_bottom_bracket = run_playoff_series(db_name, winner_conf2_2_7_seed, winner_conf2_3_6_seed , current_season)
    
    #Conference Finals
    conference1_winner = run_playoff_series(db_name, winner_conf1_top_bracket, winner_conf1_bottom_bracket, current_season)
    conference2_winner = run_playoff_series(db_name, winner_conf2_top_bracket, winner_conf2_bottom_bracket, current_season)

    #Finals
    finals_winner = run_playoff_series(db_name, conference1_winner, conference2_winner, current_season)

    return finals_winner



