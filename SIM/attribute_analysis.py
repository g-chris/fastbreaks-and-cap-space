"""
Attribute-Based Team Comparison and Analysis Tools
"""
import random


def compare_teams_by_attribute(home_team_id, away_team_id, conn):
    """
    Compare teams across all individual attributes
    
    Returns a detailed breakdown showing which team has advantage in each area
    """
    cursor = conn.cursor()
    
    attributes = [
        'attribute_strength',
        'attribute_dexterity', 
        'attribute_constitution',
        'attribute_intelligence',
        'attribute_shooting',
        'attribute_defense'
    ]
    
    comparison = {
        'home_team_id': home_team_id,
        'away_team_id': away_team_id,
        'attributes': {}
    }
    
    for attr in attributes:
        # Get home team total
        cursor.execute(f"""
            SELECT SUM({attr}) as total
            FROM team_{home_team_id}_roster
        """)
        home_total = cursor.fetchone()[0] or 0
        
        # Get away team total
        cursor.execute(f"""
            SELECT SUM({attr}) as total
            FROM team_{away_team_id}_roster
        """)
        away_total = cursor.fetchone()[0] or 0
        
        comparison['attributes'][attr] = {
            'home': home_total,
            'away': away_total,
            'advantage': 'home' if home_total > away_total else 'away' if away_total > home_total else 'even',
            'difference': abs(home_total - away_total)
        }
    
    return comparison


def simulate_attribute_matchup(home_attr, away_attr, num_rolls=10):
    """
    Simulate head-to-head matchup for a specific attribute
    
    Args:
        home_attr: Home team attribute value
        away_attr: Away team attribute value
        num_rolls: Number of simulated confrontations
    
    Returns:
        dict with win counts
    """
    home_modifier = min(max(home_attr // 50, 0), 10)
    away_modifier = min(max(away_attr // 50, 0), 10)
    
    results = {'home_wins': 0, 'away_wins': 0, 'ties': 0}
    
    for _ in range(num_rolls):
        home_roll = random.randint(1, 6) + home_modifier
        away_roll = random.randint(1, 6) + away_modifier
        
        if home_roll > away_roll:
            results['home_wins'] += 1
        elif away_roll > home_roll:
            results['away_wins'] += 1
        else:
            results['ties'] += 1
    
    return results


def offense_vs_defense_preview(home_team_id, away_team_id, conn, simulations=100):
    """
    Preview offensive vs defensive matchups between teams
    
    Shows expected performance when each team has the ball
    """
    cursor = conn.cursor()
    
    # Get offensive ratings (shooting + dexterity + intelligence)
    cursor.execute(f"""
        SELECT 
            SUM(attribute_shooting) as shooting,
            SUM(attribute_dexterity) as dexterity,
            SUM(attribute_intelligence) as intelligence
        FROM team_{home_team_id}_roster
    """)
    home_off = cursor.fetchone()
    home_offense = sum(home_off)
    
    cursor.execute(f"""
        SELECT 
            SUM(attribute_shooting) as shooting,
            SUM(attribute_dexterity) as dexterity,
            SUM(attribute_intelligence) as intelligence
        FROM team_{away_team_id}_roster
    """)
    away_off = cursor.fetchone()
    away_offense = sum(away_off)
    
    # Get defensive ratings (defense + constitution + strength)
    cursor.execute(f"""
        SELECT 
            SUM(attribute_defense) as defense,
            SUM(attribute_constitution) as constitution,
            SUM(attribute_strength) as strength
        FROM team_{home_team_id}_roster
    """)
    home_def = cursor.fetchone()
    home_defense = sum(home_def)
    
    cursor.execute(f"""
        SELECT 
            SUM(attribute_defense) as defense,
            SUM(attribute_constitution) as constitution,
            SUM(attribute_strength) as strength
        FROM team_{away_team_id}_roster
    """)
    away_def = cursor.fetchone()
    away_defense = sum(away_def)
    
    # Simulate matchups
    home_off_vs_away_def = simulate_attribute_matchup(home_offense, away_defense, simulations)
    away_off_vs_home_def = simulate_attribute_matchup(away_offense, home_defense, simulations)
    
    return {
        'home_offense': home_offense,
        'home_defense': home_defense,
        'away_offense': away_offense,
        'away_defense': away_defense,
        'home_possessions_expected': home_off_vs_away_def,
        'away_possessions_expected': away_off_vs_home_def,
        'prediction': {
            'home_scoring_efficiency': home_off_vs_away_def['home_wins'] / simulations,
            'away_scoring_efficiency': away_off_vs_home_def['home_wins'] / simulations
        }
    }


def print_matchup_preview(home_team_id, away_team_id, conn):
    """
    Print a formatted preview of the matchup
    """
    print(f"\n{'='*60}")
    print(f"MATCHUP PREVIEW: Team {home_team_id} (Home) vs Team {away_team_id} (Away)")
    print(f"{'='*60}\n")
    
    # Attribute comparison
    comparison = compare_teams_by_attribute(home_team_id, away_team_id, conn)
    print("ATTRIBUTE BREAKDOWN:")
    print(f"{'Attribute':<25} {'Home':<10} {'Away':<10} {'Advantage':<10}")
    print("-" * 60)
    
    for attr, values in comparison['attributes'].items():
        attr_name = attr.replace('attribute_', '').title()
        advantage = values['advantage'].upper()
        print(f"{attr_name:<25} {values['home']:<10} {values['away']:<10} {advantage:<10}")
    
    print("\n" + "="*60)
    
    # Offensive/Defensive matchup
    matchup = offense_vs_defense_preview(home_team_id, away_team_id, conn, simulations=100)
    print("\nOFFENSIVE vs DEFENSIVE MATCHUP:")
    print(f"Home Offense Rating: {matchup['home_offense']}")
    print(f"Home Defense Rating: {matchup['home_defense']}")
    print(f"Away Offense Rating: {matchup['away_offense']}")
    print(f"Away Defense Rating: {matchup['away_defense']}")
    
    print(f"\nExpected Scoring Efficiency:")
    print(f"Home Team: {matchup['prediction']['home_scoring_efficiency']:.1%}")
    print(f"Away Team: {matchup['prediction']['away_scoring_efficiency']:.1%}")
    print("="*60 + "\n")


def dice_roll_simulator():
    """
    Interactive function to test dice rolling mechanics
    """
    print("\nDICE ROLL SIMULATOR")
    print("Testing 1d6 + modifier system\n")
    
    modifiers = [0, 2, 5, 8, 10]
    
    for mod in modifiers:
        rolls = [random.randint(1, 6) + mod for _ in range(10)]
        avg = sum(rolls) / len(rolls)
        print(f"Modifier +{mod}: Rolls = {rolls}")
        print(f"  Average: {avg:.1f}, Min: {min(rolls)}, Max: {max(rolls)}\n")


if __name__ == "__main__":
    print("Attribute Comparison Tools loaded successfully")
    print("\nAvailable functions:")
    print("- compare_teams_by_attribute(home_id, away_id, conn)")
    print("- simulate_attribute_matchup(home_attr, away_attr, num_rolls)")
    print("- offense_vs_defense_preview(home_id, away_id, conn)")
    print("- print_matchup_preview(home_id, away_id, conn)")
    print("- dice_roll_simulator()")
    
    print("\n" + "="*60)
    dice_roll_simulator()