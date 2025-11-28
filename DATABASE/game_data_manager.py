#Create fact tables for individual player and game results
import sqlite3

def create_fact_game_results(db_name):
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create a table (example table: dim_teams)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fact_game_results (
    game_id INTEGER PRIMARY KEY,
    season_id INTEGER,
    game_day INTEGER,
    home_team_id INTEGER,
    away_team_id INTEGER,
    home_score INTEGER,
    away_score INTEGER,
    winner_team_id INTEGER,
    losing_team_id INTEGER,
    ot_count INTEGER,
    FOREIGN KEY (home_team_id) REFERENCES dim_teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES dim_teams(team_id)
);
    ''')

    # Commit the changes
    conn.commit()
    conn.close()

def record_game_results(db_name, game_id, season_id, game_day,
                        home_team_id, away_team_id, home_score, away_score, winner_team_id, losing_team_id, ot_count):
     
      # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(db_name)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()


    cursor.execute('''
            INSERT INTO fact_game_results (
                game_id, season_id, game_day, home_team_id, away_team_id, home_score, away_score, winner_team_id, losing_team_id, ot_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            game_id, season_id, game_day, home_team_id, away_team_id, home_score, away_score, winner_team_id, losing_team_id, ot_count
        ))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def create_fact_player_game_stats(db_name):
    """Create table to store individual player game statistics"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fact_player_game_stats (
            stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            team_id INTEGER NOT NULL,
            minutes_played INTEGER DEFAULT 0,
            points INTEGER DEFAULT 0,
            rebounds INTEGER DEFAULT 0,
            assists INTEGER DEFAULT 0,
            steals INTEGER DEFAULT 0,
            blocks INTEGER DEFAULT 0,
            turnovers INTEGER DEFAULT 0,
            two_point_makes INTEGER DEFAULT 0,
            two_point_attempts INTEGER DEFAULT 0,
            three_point_makes INTEGER DEFAULT 0,
            three_point_attempts INTEGER DEFAULT 0,
            field_goal_attempts INTEGER DEFAULT 0,
            field_goal_makes INTEGER DEFAULT 0,
            FOREIGN KEY (game_id) REFERENCES fact_game_results(game_id),
            FOREIGN KEY (player_id) REFERENCES dim_players(player_id),
            FOREIGN KEY (team_id) REFERENCES dim_teams(team_id),
            UNIQUE(game_id, player_id)
        )
    ''')
    
    conn.commit()
    conn.close()

def record_player_game_stats(db_name, game_id, player_id, team_id, stats_dict):
    """Record or update player statistics for a game"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO fact_player_game_stats (
            game_id, player_id, team_id, minutes_played, points, rebounds, 
            assists, steals, blocks, turnovers, two_point_makes, two_point_attempts,
            three_point_makes, three_point_attempts, field_goal_attempts, field_goal_makes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(game_id, player_id) DO UPDATE SET
            points = points + excluded.points,
            rebounds = rebounds + excluded.rebounds,
            assists = assists + excluded.assists,
            steals = steals + excluded.steals,
            blocks = blocks + excluded.blocks,
            turnovers = turnovers + excluded.turnovers,
            two_point_makes = two_point_makes + excluded.two_point_makes,
            two_point_attempts = two_point_attempts + excluded.two_point_attempts,
            three_point_makes = three_point_makes + excluded.three_point_makes,
            three_point_attempts = three_point_attempts + excluded.three_point_attempts,
            field_goal_attempts = field_goal_attempts + excluded.field_goal_attempts,
            field_goal_makes = field_goal_makes + excluded.field_goal_makes,
            minutes_played = excluded.minutes_played
    ''', (
        game_id, player_id, team_id,
        stats_dict.get('minutes_played', 0),
        stats_dict.get('points', 0),
        stats_dict.get('rebounds', 0),
        stats_dict.get('assists', 0),
        stats_dict.get('steals', 0),
        stats_dict.get('blocks', 0),
        stats_dict.get('turnovers', 0),
        stats_dict.get('two_point_makes', 0),
        stats_dict.get('two_point_attempts', 0),
        stats_dict.get('three_point_makes', 0),
        stats_dict.get('three_point_attempts', 0),
        stats_dict.get('field_goal_attempts', 0),
        stats_dict.get('field_goal_makes', 0)
    ))
    
    conn.commit()
    conn.close()
    
def record_game_with_player_stats(db_name, game_id, season_id, game_day,
                                  home_team_id, away_team_id, 
                                  home_score, away_score, 
                                  winner_team_id, losing_team_id, ot_count,
                                  home_player_stats, away_player_stats):
    """
    Record both game results and all player stats in one function
    
    home_player_stats: dict of {player_id: stats_dict}
    away_player_stats: dict of {player_id: stats_dict}
    """
    # Record game results
    record_game_results(db_name, game_id, season_id, game_day,
                       home_team_id, away_team_id, home_score, away_score,
                       winner_team_id, losing_team_id, ot_count)
    
    # Record home team player stats
    for player_id, stats in home_player_stats.items():
        record_player_game_stats(db_name, game_id, player_id, home_team_id, stats)
    
    # Record away team player stats
    for player_id, stats in away_player_stats.items():
        record_player_game_stats(db_name, game_id, player_id, away_team_id, stats)
