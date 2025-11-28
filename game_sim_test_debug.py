import sqlite3
from SIM.game_sim_engine_improved import simulate_game_with_player_stats
from SIM.attribute_analysis import print_matchup_preview

def debug_single_game(home_team_id, away_team_id, conn, max_possessions=20):
    """
    Run a single game with detailed debug output for each possession
    
    Parameters:
        home_team_id: ID of home team
        away_team_id: ID of away team
        conn: Database connection
        max_possessions: Number of possessions to show in detail (default 20, set to None for all)
    """
    print("=" * 80)
    print(f"DEBUG MODE: Team {home_team_id} (Home) vs Team {away_team_id} (Away)")
    print("=" * 80)
    
    # Run the simulation
    home_score, away_score, ot_count, home_stats, away_stats, possession_log = \
        simulate_game_with_player_stats(home_team_id, away_team_id, conn)
    
    print(f"\nFINAL SCORE: {home_score} - {away_score}")
    if ot_count > 0:
        print(f"Overtime periods: {ot_count}")
    
    # Show possession-by-possession breakdown
    print("\n" + "=" * 80)
    print("POSSESSION-BY-POSSESSION BREAKDOWN")
    print("=" * 80)
    
    possessions_to_show = len(possession_log) if max_possessions is None else min(max_possessions, len(possession_log))
    
    for i, poss in enumerate(possession_log[:possessions_to_show]):
        print(f"\n--- Possession {poss['possession_number']} ---")
        print(f"Offense: Team {poss['offense_team']} | Defense: Team {poss['defense_team']}")
        print(f"Offense Roll: {poss['offense_roll']} | Defense Roll: {poss['defense_roll']}")
        print(f"Outcome: {poss['outcome']}")
        
        if 'shot_type' in poss:
            print(f"Shot Type: {poss['shot_type']}")
        
        if 'scorer' in poss:
            print(f"Scorer: Player {poss['scorer']}")
        
        if 'assist' in poss:
            print(f"Assist: Player {poss['assist']}")
        
        if 'rebounder' in poss:
            print(f"Rebounder: {poss['rebounder'][0]} - Player {poss['rebounder'][1]}")
        
        if 'block' in poss:
            print(f"Block: Player {poss['block']}")
        
        print(f"Points: {poss['points']}")
    
    if possessions_to_show < len(possession_log):
        print(f"\n... ({len(possession_log) - possessions_to_show} more possessions) ...")
    
    # Show shooting statistics summary
    print("\n" + "=" * 80)
    print("SHOOTING BREAKDOWN")
    print("=" * 80)
    
    home_3pa = sum(s['three_point_attempts'] for s in home_stats.values())
    home_3pm = sum(s['three_point_makes'] for s in home_stats.values())
    home_2pa = sum(s['two_point_attempts'] for s in home_stats.values())
    home_2pm = sum(s['two_point_makes'] for s in home_stats.values())
    
    away_3pa = sum(s['three_point_attempts'] for s in away_stats.values())
    away_3pm = sum(s['three_point_makes'] for s in away_stats.values())
    away_2pa = sum(s['two_point_attempts'] for s in away_stats.values())
    away_2pm = sum(s['two_point_makes'] for s in away_stats.values())
    
    print(f"\nHome Team (Team {home_team_id}):")
    print(f"  2-Point: {home_2pm}/{home_2pa} ({(home_2pm/home_2pa*100) if home_2pa > 0 else 0:.1f}%)")
    print(f"  3-Point: {home_3pm}/{home_3pa} ({(home_3pm/home_3pa*100) if home_3pa > 0 else 0:.1f}%)")
    print(f"  Total FG: {home_2pm + home_3pm}/{home_2pa + home_3pa}")
    
    print(f"\nAway Team (Team {away_team_id}):")
    print(f"  2-Point: {away_2pm}/{away_2pa} ({(away_2pm/away_2pa*100) if away_2pa > 0 else 0:.1f}%)")
    print(f"  3-Point: {away_3pm}/{away_3pa} ({(away_3pm/away_3pa*100) if away_3pa > 0 else 0:.1f}%)")
    print(f"  Total FG: {away_2pm + away_3pm}/{away_2pa + away_3pa}")
    
    # Show top performers
    print("\n" + "=" * 80)
    print("TOP PERFORMERS")
    print("=" * 80)
    
    print(f"\nHome Team (Team {home_team_id}) - Top 5 Scorers:")
    home_scorers = sorted(home_stats.items(), key=lambda x: x[1]['points'], reverse=True)[:5]
    for player_id, stats in home_scorers:
        if stats['points'] > 0:
            print(f"  Player {player_id}: {stats['points']} pts, {stats['rebounds']} reb, {stats['assists']} ast, "
                  f"{stats['field_goal_makes']}/{stats['field_goal_attempts']} FG, "
                  f"{stats['three_point_makes']}/{stats['three_point_attempts']} 3PT")
    
    print(f"\nAway Team (Team {away_team_id}) - Top 5 Scorers:")
    away_scorers = sorted(away_stats.items(), key=lambda x: x[1]['points'], reverse=True)[:5]
    for player_id, stats in away_scorers:
        if stats['points'] > 0:
            print(f"  Player {player_id}: {stats['points']} pts, {stats['rebounds']} reb, {stats['assists']} ast, "
                  f"{stats['field_goal_makes']}/{stats['field_goal_attempts']} FG, "
                  f"{stats['three_point_makes']}/{stats['three_point_attempts']} 3PT")
    
    return home_score, away_score, ot_count, possession_log


def debug_shot_selection_only(home_team_id, away_team_id, conn, num_possessions=50):
    """
    Focus specifically on shot selection to debug 3-point attempt logic
    """
    print("=" * 80)
    print(f"SHOT SELECTION DEBUG: Team {home_team_id} (Home) vs Team {away_team_id} (Away)")
    print("=" * 80)
    
    # Run the simulation
    home_score, away_score, ot_count, home_stats, away_stats, possession_log = \
        simulate_game_with_player_stats(home_team_id, away_team_id, conn)
    
    print(f"\nAnalyzing shot selection from {len(possession_log)} total possessions...\n")
    
    shot_attempts = [p for p in possession_log if 'shot_type' in p]
    
    print(f"Total shot attempts: {len(shot_attempts)}")
    
    three_pt_attempts = [p for p in shot_attempts if '3pt' in p.get('shot_type', '')]
    two_pt_attempts = [p for p in shot_attempts if '2pt' in p.get('shot_type', '')]
    
    print(f"Three-point attempts: {len(three_pt_attempts)}")
    print(f"Two-point attempts: {len(two_pt_attempts)}")
    
    if len(three_pt_attempts) == 0:
        print("\n⚠️  WARNING: NO THREE-POINT ATTEMPTS FOUND!")
        print("\nShowing first 20 shot attempts to debug:")
        for i, poss in enumerate(shot_attempts[:20]):
            print(f"\nShot {i+1}:")
            print(f"  Possession: {poss['possession_number']}")
            print(f"  Offense Team: {poss['offense_team']}")
            print(f"  Outcome: {poss['outcome']}")
            print(f"  Shot Type: {poss.get('shot_type', 'NOT RECORDED')}")
            print(f"  Points: {poss['points']}")
    else:
        print("\n✓ Three-point attempts are working!")
        print(f"\nThree-point shooting percentage: {len(three_pt_attempts) / len(shot_attempts) * 100:.1f}%")


if __name__ == "__main__":
    # Connect to database
    conn = sqlite3.connect('league01.db')
    
    # Option 1: Full debug of single game (first 20 possessions)
    print("\n\n")
    print("OPTION 1: DETAILED POSSESSION BREAKDOWN")
    print("=" * 80)
    debug_single_game(1, 1, conn, max_possessions=20)
    
    # Option 2: Focus on shot selection issue
    print("\n\n\n")
    print("OPTION 2: SHOT SELECTION DEBUG")
    print("=" * 80)
    debug_shot_selection_only(1, 1, conn)
    
    # Option 3: Quick multi-game test
    print("\n\n\n")
    print("OPTION 3: MULTI-GAME TEST")
    print("=" * 80)
    print("\nSimulating 5 games to check consistency:")
    for i in range(5):
        home, away, ot, home_stats, away_stats, log = simulate_game_with_player_stats(1, 1, conn)
        ot_text = f" ({ot} OT)" if ot > 0 else ""
        
        total_3pa = sum(s['three_point_attempts'] for s in home_stats.values()) + \
                    sum(s['three_point_attempts'] for s in away_stats.values())
        total_2pa = sum(s['two_point_attempts'] for s in home_stats.values()) + \
                    sum(s['two_point_attempts'] for s in away_stats.values())
        
        print(f"Game {i+1}: {home}-{away}{ot_text} | Shots: {total_2pa} 2PT, {total_3pa} 3PT")
    
    conn.close()