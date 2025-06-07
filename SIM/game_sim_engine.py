#Take a View for each team and generate scores
#Publish game stats for each player to a fact table


import random

def game_sim(home_team_id, away_team_id, conn):
    ot_count = 0
    cursor = conn.cursor()

    def get_team_score(team_id):
        view_name = f"team_{team_id}_roster"
        cursor.execute(f"SELECT overall_score FROM {view_name}")
        player_ratings = cursor.fetchall()
        base_score = sum([rating[0] for rating in player_ratings])
        return base_score
    
    home_random_bonus = random.randint(5, 20)
    away_random_bonus = random.randint(1, 20)

    home_scaled_score = round(get_team_score(home_team_id) / 3.7)
    away_scaled_score = round(get_team_score(away_team_id) / 3.7)

    home_score = home_scaled_score + home_random_bonus
    away_score = away_scaled_score + away_random_bonus

    while home_score == away_score:
        ot_count = ot_count + 1
        home_score = home_score + round(random.randint(5, 20)/2)
        away_score = away_score + round(random.randint(1, 20)/2)

        # if ot_count == 5:
        #     if random.randint(1, 2) == 1:
        #         home_score = home_score + 1
        #     else:
        #         away_score = away_score + 1
        
    return home_score, away_score, ot_count

