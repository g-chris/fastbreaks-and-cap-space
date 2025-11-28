# Enhanced Game Simulation Engine with Individual Player Statistics
# Builds on the attribute-based possession simulation from the previous version
# Now tracks individual player stats for points, rebounds, assists, steals, blocks, etc.

import random
import sqlite3


def roll_d6():
    """Roll a single 6-sided die"""
    return random.randint(1, 6)


def get_team_roster_with_attributes(conn, team_id):
    """
    Fetch all players for a team with their attributes
    Returns list of dicts with player_id and all attributes
    """
    cursor = conn.cursor()
    view_name = f"team_{team_id}_roster"
    
    cursor.execute(f"""
        SELECT 
            player_id,
            first_name,
            last_name,
            attribute_strength,
            attribute_dexterity,
            attribute_constitution,
            attribute_intelligence,
            attribute_shooting,
            attribute_defense
        FROM {view_name}
    """)
    
    columns = [col[0] for col in cursor.description]
    players = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    return players


def calculate_team_ratings(team_roster):
    """
    Calculate offensive and defensive ratings for a team
    Returns: (offensive_rating, defensive_rating)
    """
    # Offensive rating: Shooting + Dexterity + Intelligence
    offensive_rating = sum(
        p['attribute_shooting'] + p['attribute_dexterity'] + p['attribute_intelligence']
        for p in team_roster
    )
    
    # Defensive rating: Defense + Constitution + Strength
    defensive_rating = sum(
        p['attribute_defense'] + p['attribute_constitution'] + p['attribute_strength']
        for p in team_roster
    )
    
    return offensive_rating, defensive_rating


def get_scorer_weights(team_roster):
    """Players with high SHOOTING get ball more often for scoring"""
    return {
        p['player_id']: max(1, p['attribute_shooting']) 
        for p in team_roster
    }


def get_rebounder_weights(team_roster):
    """Players with high STRENGTH + CONSTITUTION get more rebounds"""
    return {
        p['player_id']: max(1, p['attribute_strength'] + p['attribute_constitution']) 
        for p in team_roster
    }


def get_assist_weights(team_roster):
    """Players with high INTELLIGENCE + DEXTERITY distribute ball better"""
    return {
        p['player_id']: max(1, p['attribute_intelligence'] + p['attribute_dexterity']) 
        for p in team_roster
    }


def get_defender_weights(team_roster):
    """Players with high DEFENSE get more steals/blocks"""
    return {
        p['player_id']: max(1, p['attribute_defense']) 
        for p in team_roster
    }


def select_weighted_player(weights):
    """
    Select a player_id based on weighted probabilities
    weights: dict of {player_id: weight}
    """
    if not weights:
        return None
    
    total_weight = sum(weights.values())
    if total_weight == 0:
        return random.choice(list(weights.keys()))
    
    rand = random.uniform(0, total_weight)
    cumulative = 0
    
    for player_id, weight in weights.items():
        cumulative += weight
        if rand <= cumulative:
            return player_id
    
    return list(weights.keys())[-1]


def initialize_player_stats():
    """Initialize empty stat dictionary for a player"""
    return {
        'minutes_played': 0,
        'points': 0,
        'rebounds': 0,
        'assists': 0,
        'steals': 0,
        'blocks': 0,
        'turnovers': 0,
        'two_point_makes': 0,
        'two_point_attempts': 0,
        'three_point_makes': 0,
        'three_point_attempts': 0,
        'field_goal_attempts': 0,
        'field_goal_makes': 0
    }


def simulate_possession(offense_roster, defense_roster, offense_rating, defense_rating, game_stats):
    """
    Simulate a single possession with player stat attribution
    
    Returns: (points_scored, possession_log_entry)
    Updates game_stats dict in place with individual player stats
    """
    # Calculate modifiers (0-10 scale)
    offensive_modifier = min(10, offense_rating // 120)
    defensive_modifier = min(10, defense_rating // 120)
    
    # Roll for possession outcome
    offense_roll = roll_d6() + offensive_modifier
    defense_roll = roll_d6() + defensive_modifier
    
    possession_result = {
        'offense_team': 'offense',
        'defense_team': 'defense',
        'offense_roll': offense_roll,
        'defense_roll': defense_roll,
        'outcome': '',
        'points': 0
    }
    
    # Determine possession outcome
    if defense_roll > offense_roll + 2:
        # TURNOVER - Defensive player gets steal
        possession_result['outcome'] = 'turnover'
        possession_result['points'] = 0
        
        # Attribute turnover to random offensive player (weighted by dexterity - lower is worse)
        inverse_dex_weights = {p['player_id']: max(1, 20 - p['attribute_dexterity']) for p in offense_roster}
        turnover_player = select_weighted_player(inverse_dex_weights)
        game_stats[turnover_player]['turnovers'] += 1
        
        # Attribute steal to defensive player
        steal_player = select_weighted_player(get_defender_weights(defense_roster))
        game_stats[steal_player]['steals'] += 1
        
    elif defense_roll > offense_roll:
        # TOUGH SHOT - Lower shooting percentage
        possession_result['outcome'] = 'tough_shot'
        points = simulate_shot_attempt(offense_roster, defense_roster, game_stats, 
                                       shot_quality='tough', possession_result=possession_result)
        possession_result['points'] = points
        
    else:
        # Determine shot quality based on margin
        margin = offense_roll - defense_roll
        if margin >= 4:
            shot_quality = 'great'
        else:
            shot_quality = 'normal'
        
        possession_result['outcome'] = f'{shot_quality}_shot'
        points = simulate_shot_attempt(offense_roster, defense_roster, game_stats, 
                                       shot_quality=shot_quality, possession_result=possession_result)
        possession_result['points'] = points
    
    return possession_result['points'], possession_result


def simulate_shot_attempt(offense_roster, defense_roster, game_stats, shot_quality, possession_result):
    """
    Simulate a shot attempt with 2pt/3pt determination and player attribution
    
    shot_quality: 'great', 'normal', or 'tough'
    Updates game_stats and possession_result in place
    Returns: points scored (0, 2, or 3)
    """
    # Determine shot type based on intelligence (3pt vs 2pt decision)
    # Higher intelligence teams take more 3-pointers
    avg_intelligence = sum(p['attribute_intelligence'] for p in offense_roster) / len(offense_roster)
    shot_selection_roll = roll_d6() + (avg_intelligence / 3)  # Intelligence modifier: ~3-5 for avg teams
    
    # About 30-35% of shots should be 3-pointers (threshold of 10)
    # With d6 (1-6) + modifier (3-5), you get 4-11, so ~40% will be >= 10
    is_three_pointer = shot_selection_roll >= 10
    
    # Select shooter (weighted by shooting attribute)
    shooter_id = select_weighted_player(get_scorer_weights(offense_roster))
    shooter = next(p for p in offense_roster if p['player_id'] == shooter_id)
    
    # Calculate shooting modifier
    team_shooting_total = sum(p['attribute_shooting'] for p in offense_roster)
    shooting_mod = team_shooting_total / 50
    
    # Roll for shot success
    shot_roll = roll_d6() + shooting_mod
    
    # Determine thresholds based on shot quality and type
    thresholds = {
        'great': {'2pt': 4, '3pt': 6},
        'normal': {'2pt': 5, '3pt': 8},
        'tough': {'2pt': 7, '3pt': 10}
    }
    
    shot_type = '3pt' if is_three_pointer else '2pt'
    threshold = thresholds[shot_quality][shot_type]
    
    # Record attempt
    if is_three_pointer:
        game_stats[shooter_id]['three_point_attempts'] += 1
    else:
        game_stats[shooter_id]['two_point_attempts'] += 1
    game_stats[shooter_id]['field_goal_attempts'] += 1
    
    # Check if shot is made
    if shot_roll >= threshold:
        # MADE SHOT
        points = 3 if is_three_pointer else 2
        
        # Record make
        if is_three_pointer:
            game_stats[shooter_id]['three_point_makes'] += 1
            possession_result['shot_type'] = '3pt_make'
        else:
            game_stats[shooter_id]['two_point_makes'] += 1
            possession_result['shot_type'] = '2pt_make'
        
        game_stats[shooter_id]['field_goal_makes'] += 1
        game_stats[shooter_id]['points'] += points
        possession_result['scorer'] = shooter_id
        
        # Possible assist (higher chance for 3-pointers)
        assist_chance = 0.70 if is_three_pointer else 0.60
        if random.random() < assist_chance:
            # Find assist player (not the scorer)
            assist_weights = get_assist_weights(offense_roster)
            if shooter_id in assist_weights:
                del assist_weights[shooter_id]
            
            if assist_weights:
                assist_player = select_weighted_player(assist_weights)
                game_stats[assist_player]['assists'] += 1
                possession_result['assist'] = assist_player
        
        return points
    else:
        # MISSED SHOT - Award rebound
        possession_result['shot_type'] = f"{shot_type}_miss"
        
        # Check for block (tough shots have higher block chance)
        block_chance = 0.15 if shot_quality == 'tough' else 0.05
        if random.random() < block_chance:
            # Defensive player gets block
            blocker = select_weighted_player(get_defender_weights(defense_roster))
            game_stats[blocker]['blocks'] += 1
            game_stats[blocker]['rebounds'] += 1  # Blocks usually lead to defensive rebounds
            possession_result['block'] = blocker
        else:
            # Regular rebound - 70% defensive, 30% offensive
            if random.random() < 0.70:
                # Defensive rebound
                rebounder = select_weighted_player(get_rebounder_weights(defense_roster))
                game_stats[rebounder]['rebounds'] += 1
                possession_result['rebounder'] = ('defense', rebounder)
            else:
                # Offensive rebound
                rebounder = select_weighted_player(get_rebounder_weights(offense_roster))
                game_stats[rebounder]['rebounds'] += 1
                possession_result['rebounder'] = ('offense', rebounder)
        
        return 0


def simulate_game_with_player_stats(home_team_id, away_team_id, conn, home_court_advantage=2):
    """
    Main game simulation function with full player stat tracking
    
    Parameters:
        home_team_id: ID of home team
        away_team_id: ID of away team
        conn: Database connection
        home_court_advantage: Bonus added to home team's offensive rating (default: 2)
    
    Returns: (home_score, away_score, ot_count, home_stats, away_stats, possession_log)
    """
    # Fetch team rosters
    home_roster = get_team_roster_with_attributes(conn, home_team_id)
    away_roster = get_team_roster_with_attributes(conn, away_team_id)
    
    # Calculate team ratings
    home_off_rating, home_def_rating = calculate_team_ratings(home_roster)
    away_off_rating, away_def_rating = calculate_team_ratings(away_roster)
    
    # Apply home court advantage to home team's offense
    home_off_rating += home_court_advantage * 10  # Multiply by 10 to match the 0-10 modifier scale
    
    # Initialize player stats dictionaries
    home_stats = {p['player_id']: initialize_player_stats() for p in home_roster}
    away_stats = {p['player_id']: initialize_player_stats() for p in away_roster}
    
    # Set minutes played (simplified - all players get 48 minutes for now)
    for player_id in home_stats:
        home_stats[player_id]['minutes_played'] = 48
    for player_id in away_stats:
        away_stats[player_id]['minutes_played'] = 48
    
    # Simulate possessions
    home_score = 0
    away_score = 0
    possession_log = []
    
    # Regulation: ~100 possessions per team
    total_possessions = 200
    
    for i in range(total_possessions):
        if i % 2 == 0:
            # Home team offense
            points, log_entry = simulate_possession(
                home_roster, away_roster, home_off_rating, away_def_rating, 
                {**home_stats, **away_stats}
            )
            home_score += points
            log_entry['possession_number'] = i + 1
            log_entry['offense_team'] = home_team_id
            log_entry['defense_team'] = away_team_id
        else:
            # Away team offense
            points, log_entry = simulate_possession(
                away_roster, home_roster, away_off_rating, home_def_rating,
                {**away_stats, **home_stats}
            )
            away_score += points
            log_entry['possession_number'] = i + 1
            log_entry['offense_team'] = away_team_id
            log_entry['defense_team'] = home_team_id
        
        possession_log.append(log_entry)
    
    # Handle overtime if needed
    ot_count = 0
    while home_score == away_score:
        ot_count += 1
        # Overtime: 10 possessions per team
        ot_possessions = 20
        
        for i in range(ot_possessions):
            if i % 2 == 0:
                points, log_entry = simulate_possession(
                    home_roster, away_roster, home_off_rating, away_def_rating,
                    {**home_stats, **away_stats}
                )
                home_score += points
                log_entry['possession_number'] = f"OT{ot_count}-{i+1}"
                log_entry['offense_team'] = home_team_id
                log_entry['defense_team'] = away_team_id
            else:
                points, log_entry = simulate_possession(
                    away_roster, home_roster, away_off_rating, home_def_rating,
                    {**away_stats, **home_stats}
                )
                away_score += points
                log_entry['possession_number'] = f"OT{ot_count}-{i+1}"
                log_entry['offense_team'] = away_team_id
                log_entry['defense_team'] = home_team_id
            
            possession_log.append(log_entry)
        
        # Safety: max 5 overtimes, then sudden death
        if ot_count >= 5 and home_score == away_score:
            if random.random() < 0.5:
                home_score += 1
            else:
                away_score += 1
    
    return home_score, away_score, ot_count, home_stats, away_stats, possession_log


def game_sim(home_team_id, away_team_id, conn, home_court_advantage=2):
    """
    Wrapper function to maintain compatibility with existing code
    
    Parameters:
        home_team_id: ID of home team
        away_team_id: ID of away team  
        conn: Database connection
        home_court_advantage: Bonus for home team (default: 2)
    
    Returns: (home_score, away_score, ot_count)
    """
    home_score, away_score, ot_count, home_stats, away_stats, possession_log = \
        simulate_game_with_player_stats(home_team_id, away_team_id, conn, home_court_advantage)
    
    return home_score, away_score, ot_count


# For testing/debugging
if __name__ == "__main__":
    # This section is for testing only
    test_db = "league01.db"
    
    try:
        conn = sqlite3.connect(test_db)
        
        # Test with team IDs 1 and 2, with home court advantage of 2
        print("Simulating game between Team 1 (home) and Team 2 (away)...")
        print("Home court advantage: +2 to home team offense")
        home_score, away_score, ot_count, home_stats, away_stats, log = \
            simulate_game_with_player_stats(1, 2, conn, home_court_advantage=2)
        
        print(f"\nFinal Score: Team 1: {home_score}, Team 2: {away_score}")
        if ot_count > 0:
            print(f"Overtimes: {ot_count}")
        
        print("\n=== HOME TEAM STATS ===")
        for player_id, stats in home_stats.items():
            if stats['points'] > 0 or stats['rebounds'] > 0:
                print(f"Player {player_id}: {stats['points']} pts, "
                      f"{stats['rebounds']} reb, {stats['assists']} ast, "
                      f"{stats['steals']} stl, {stats['blocks']} blk, "
                      f"{stats['turnovers']} to, "
                      f"{stats['field_goal_makes']}/{stats['field_goal_attempts']} FG "
                      f"({stats['two_point_makes']}/{stats['two_point_attempts']} 2PT, "
                      f"{stats['three_point_makes']}/{stats['three_point_attempts']} 3PT)")
        
        print("\n=== AWAY TEAM STATS ===")
        for player_id, stats in away_stats.items():
            if stats['points'] > 0 or stats['rebounds'] > 0:
                print(f"Player {player_id}: {stats['points']} pts, "
                      f"{stats['rebounds']} reb, {stats['assists']} ast, "
                      f"{stats['steals']} stl, {stats['blocks']} blk, "
                      f"{stats['turnovers']} to, "
                      f"{stats['field_goal_makes']}/{stats['field_goal_attempts']} FG "
                      f"({stats['two_point_makes']}/{stats['two_point_attempts']} 2PT, "
                      f"{stats['three_point_makes']}/{stats['three_point_attempts']} 3PT)")
        
        conn.close()
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()