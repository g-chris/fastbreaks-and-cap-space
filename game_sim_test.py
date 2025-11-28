import sqlite3
from SIM.game_sim_engine_improved import game_sim
from SIM.attribute_analysis import print_matchup_preview

conn = sqlite3.connect('league01.db')

# Preview the matchup
print_matchup_preview(1, 2, conn)

# Simulate 5 games
print("\nSimulating 5 games:")
for i in range(10):
    home, away, ot = game_sim(1, 2, conn)
    ot_text = f" ({ot} OT)" if ot > 0 else ""
    print(f"Game {i+1}: {home}-{away}{ot_text}")