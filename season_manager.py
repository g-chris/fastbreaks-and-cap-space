import itertools

def generate_team_matchups(teams):
    matchups = list(itertools.combinations(teams, 2))
    return matchups + [(team2, team1) for (team1, team2) in matchups]

def schedule_season(teams, num_games):
    matchups = generate_team_matchups(teams)
    num_teams = len(teams)
    num_rounds = (num_teams - 1) * num_games
    schedule = [[] for _ in range(num_rounds)]

    # Distribute matchups evenly across rounds
    for i, matchup in enumerate(matchups):
        for j in range(num_games):
            schedule[(i * num_games + j) % num_rounds].append(matchup)

    return schedule
S
# Example usage
num_teams = 30
num_games = 82
teams = [f"Team {i}" for i in range(1, num_teams + 1)]
season_schedule = schedule_season(teams, num_games)
print(season_schedule)

