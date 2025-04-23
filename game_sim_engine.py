#Take a View for each team and generate scores
#Publish game stats for each player to a fact table


def game_sim(home_team_id, away_team_id, conn):
    cursor = conn.cursor()

    def get_team_score(team_id):
        view_name = f"team_{team_id}_roster"
        cursor.execute(f"SELECT overall_score FROM {view_name}")
        player_ratings = cursor.fetchall()
        score = sum([rating[0] for rating in player_ratings])
        return int(score)  # round to int for score

    home_score = get_team_score(home_team_id)
    away_score = get_team_score(away_team_id)

    return home_score, away_score
