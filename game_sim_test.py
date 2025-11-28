import sqlite3
from SIM.game_sim_engine_improved import game_sim, simulate_game_with_player_stats
from SIM.attribute_analysis import print_matchup_preview

conn = sqlite3.connect('league01.db')

# Preview the matchup
print_matchup_preview(1, 2, conn)

# Simulate 10 games with detailed stats
print("\nSimulating 10 games:")
print("=" * 80)

# Track aggregate stats
total_home_score = 0
total_away_score = 0
total_2pm = 0
total_2pa = 0
total_3pm = 0
total_3pa = 0
total_fgm = 0
total_fga = 0
overtime_games = 0

for i in range(10):
    # Use the full simulation to get stats
    home_score, away_score, ot_count, home_stats, away_stats, possession_log = \
        simulate_game_with_player_stats(1, 2, conn)
    
    # Calculate shooting stats for this game
    home_2pm = sum(s['two_point_makes'] for s in home_stats.values())
    home_2pa = sum(s['two_point_attempts'] for s in home_stats.values())
    home_3pm = sum(s['three_point_makes'] for s in home_stats.values())
    home_3pa = sum(s['three_point_attempts'] for s in home_stats.values())
    
    away_2pm = sum(s['two_point_makes'] for s in away_stats.values())
    away_2pa = sum(s['two_point_attempts'] for s in away_stats.values())
    away_3pm = sum(s['three_point_makes'] for s in away_stats.values())
    away_3pa = sum(s['three_point_attempts'] for s in away_stats.values())
    
    game_2pm = home_2pm + away_2pm
    game_2pa = home_2pa + away_2pa
    game_3pm = home_3pm + away_3pm
    game_3pa = home_3pa + away_3pa
    game_fgm = game_2pm + game_3pm
    game_fga = game_2pa + game_3pa
    
    # Update totals
    total_home_score += home_score
    total_away_score += away_score
    total_2pm += game_2pm
    total_2pa += game_2pa
    total_3pm += game_3pm
    total_3pa += game_3pa
    total_fgm += game_fgm
    total_fga += game_fga
    
    if ot_count > 0:
        overtime_games += 1
    
    # Calculate percentages for this game
    fg_pct = (game_fgm / game_fga * 100) if game_fga > 0 else 0
    two_pct = (game_2pm / game_2pa * 100) if game_2pa > 0 else 0
    three_pct = (game_3pm / game_3pa * 100) if game_3pa > 0 else 0
    three_rate = (game_3pa / game_fga * 100) if game_fga > 0 else 0
    
    ot_text = f" ({ot_count} OT)" if ot_count > 0 else ""
    
    print(f"Game {i+1:2}: {home_score:3}-{away_score:<3}{ot_text:8} | "
          f"FG: {game_fgm:2}/{game_fga:3} ({fg_pct:4.1f}%) | "
          f"2PT: {game_2pm:2}/{game_2pa:3} ({two_pct:4.1f}%) | "
          f"3PT: {game_3pm:2}/{game_3pa:2} ({three_pct:4.1f}%) | "
          f"3PA%: {three_rate:4.1f}%")

# Print summary statistics
print("=" * 80)
print("\nAGGREGATE STATISTICS (10 Games)")
print("=" * 80)

avg_home_score = total_home_score / 10
avg_away_score = total_away_score / 10
avg_total_score = (total_home_score + total_away_score) / 10

overall_fg_pct = (total_fgm / total_fga * 100) if total_fga > 0 else 0
overall_2pt_pct = (total_2pm / total_2pa * 100) if total_2pa > 0 else 0
overall_3pt_pct = (total_3pm / total_3pa * 100) if total_3pa > 0 else 0
overall_3pt_rate = (total_3pa / total_fga * 100) if total_fga > 0 else 0

print(f"\nScoring:")
print(f"  Average Home Score:  {avg_home_score:.1f}")
print(f"  Average Away Score:  {avg_away_score:.1f}")
print(f"  Average Total Score: {avg_total_score:.1f}")
print(f"  Overtime Games:      {overtime_games}/10")

print(f"\nShooting Percentages:")
print(f"  Overall FG%:  {total_fgm}/{total_fga} ({overall_fg_pct:.1f}%)")
print(f"  2-Point FG%:  {total_2pm}/{total_2pa} ({overall_2pt_pct:.1f}%)")
print(f"  3-Point FG%:  {total_3pm}/{total_3pa} ({overall_3pt_pct:.1f}%)")
print(f"  3PT Attempt Rate: {overall_3pt_rate:.1f}% of all shots")

print(f"\nPer Game Averages:")
print(f"  FG Made:    {total_fgm/10:.1f}")
print(f"  FG Attempt: {total_fga/10:.1f}")
print(f"  3PT Made:   {total_3pm/10:.1f}")
print(f"  3PT Attempt: {total_3pa/10:.1f}")

print("\n" + "=" * 80)
print("NBA COMPARISON (for reference)")
print("=" * 80)
print("Typical NBA Stats:")
print("  Points per game:  ~110-115")
print("  Overall FG%:      ~45-47%")
print("  2-Point FG%:      ~52-54%")
print("  3-Point FG%:      ~35-37%")
print("  3PT Attempt Rate: ~38-42%")

conn.close()