# import itertools

# def generate_team_matchups(teams):
#     matchups = list(itertools.combinations(teams, 2))
#     return matchups

# def schedule_season(teams, num_games):
#     matchups = generate_team_matchups(teams)
#     num_teams = len(teams)
#     num_rounds = num_teams - 1
#     schedule = [[] for _ in range(num_rounds)]

#     # Distribute matchups across rounds, ensuring each matchup appears exactly once
#     for i in range(num_rounds):
#         round_matchups = matchups[i:] + matchups[:i]
#         round_schedule = []
#         for j in range(num_games):
#             round_schedule.extend(round_matchups)
#         schedule[i] = round_schedule

#     return schedule


# #Example usage
# num_teams = 5
# num_games = 10
# teams = [f"Team {i}" for i in range(1, num_teams + 1)]
# season_schedule = schedule_season(teams, num_games)
# print(season_schedule)

# import random 

# def schedule_season(num_teams, num_games, hosting_limit):
#     # Initialize schedule matrix
#     schedule = [[-1] * num_games for _ in range(num_teams)]

#     # Create a list for each team containing all other team numbers
#     team_opponents = [list(range(num_teams)) for _ in range(num_teams)]

#     # Remove each team's own number from its list of opponents
#     for team in range(num_teams):
#         team_opponents[team].remove(team)

#     # Shuffle the team opponents list for randomness
#     for opponents in team_opponents:
#         random.shuffle(opponents)

#     # Iterate over each game day pair
#     for game_day in range(num_games // 2):
#         # Iterate over each team to schedule their home game
#         for home_team in range(num_teams):
#             if schedule[home_team][2 * game_day] != -1:
#                 continue  # Skip if the home team already has a scheduled game on this day

#             # Select an opponent for the home team
#             for away_team in team_opponents[home_team]:
#                 # Ensure the away team has not reached its hosting limit
#                 if schedule[away_team][2 * game_day] == -1 or schedule[away_team].count(away_team) < hosting_limit:
#                     # Schedule the home game
#                     schedule[home_team][2 * game_day] = away_team
#                     schedule[away_team][2 * game_day] = home_team
#                     # Remove the selected opponent from the list
#                     team_opponents[home_team].remove(away_team)
#                     team_opponents[away_team].remove(home_team)
#                     break  # Move to the next home team

#         # Iterate over each team to schedule their away game
#         for away_team in range(num_teams):
#             if schedule[away_team][2 * game_day + 1] != -1:
#                 continue  # Skip if the away team already has a scheduled game on this day

#             # Select an opponent for the away team
#             for home_team in team_opponents[away_team]:
#                 # Ensure the home team has not reached its hosting limit
#                 if schedule[home_team][2 * game_day + 1] == -1 or schedule[home_team].count(home_team) < hosting_limit:
#                     # Schedule the away game
#                     schedule[away_team][2 * game_day + 1] = home_team
#                     schedule[home_team][2 * game_day + 1] = away_team
#                     # Remove the selected opponent from the list
#                     team_opponents[away_team].remove(home_team)
#                     team_opponents[home_team].remove(away_team)
#                     break  # Move to the next away team

#     return schedule

# num_teams = 30
# num_games = 82
# hosting_limit = 3  # Maximum number of times a team can host the same opponent in a season
# schedule = schedule_season(num_teams, num_games, hosting_limit)

# for i, row in enumerate(schedule):
#     print(f"Team {i + 1}: {row}")


# def schedule_season(num_games, num_teams, host_limit):
#     home_game_count = num_games//2

#     away_game_count = num_games - home_game_count

#     #Create a list of lists for each team

#     #Load the list of opponents for each team's home games
#     for teams in num_teams:
#         for games in home_game_count:
#             for hosted_games in host_limit:
#                 #add each team that is not the current team

#     #Fill out each team's home matchups by randomly selecting an opponent from the list and then popping that team off the list
                
#     #Once all home matchups are set for team, make a list for each team that has its team number and game count
    
#     #Now we iterate through each team again to fill out their away schedule. 
#     #We will need to check both team's total game count each team to make sure both teams stay under the num_games

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