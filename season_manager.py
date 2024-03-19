import random

def schedule_season_v1(num_games, num_teams, host_limit):
    home_game_count = num_games // 2
    away_game_count = num_games - home_game_count

    # Initialize dictionaries to track games played between teams
    home_games_played = {team: {opponent: 0 for opponent in range(1, num_teams + 1)} for team in range(1, num_teams + 1)}
    away_games_played = {team: {opponent: 0 for opponent in range(1, num_teams + 1)} for team in range(1, num_teams + 1)}

    # Initialize schedules for home and away games
    home_schedule = {team: [] for team in range(1, num_teams + 1)}
    away_schedule = {team: [] for team in range(1, num_teams + 1)}

    # Generate schedules
    for team in range(1, num_teams + 1):
        for _ in range(home_game_count):
            opponents = [opponent for opponent in range(1, num_teams + 1) if home_games_played[team][opponent] < host_limit]
            if not opponents:
                break
            opponent = random.choice(opponents)
            home_schedule[team].append(opponent)
            home_games_played[team][opponent] += 1
            home_games_played[opponent][team] += 1

    for team in range(1, num_teams + 1):
        for _ in range(away_game_count):
            opponents = [opponent for opponent in range(1, num_teams + 1) if away_games_played[team][opponent] < host_limit and opponent not in home_schedule[team]]
            if not opponents:
                break
            opponent = random.choice(opponents)
            away_schedule[team].append(opponent)
            away_games_played[team][opponent] += 1
            away_games_played[opponent][team] += 1

    return home_schedule, away_schedule

def schedule_season_v2(league_db_name):
    print("ok")

    

def print_game_counts(home_schedule, away_schedule):
    print("Team\tHome Games\tAway Games")
    for team in home_schedule:
        home_games = len(home_schedule[team])
        away_games = len(away_schedule[team])
        print(f"{team}\t{home_games}\t\t{away_games}")

#For testing
# num_games = 82
# num_teams = 30
# host_limit = 12
# home_schedule, away_schedule = schedule_season_v1(num_games, num_teams, host_limit)
# print("Home Schedule:", home_schedule)
# print("Away Schedule:", away_schedule)

#print_game_counts(home_schedule, away_schedule)