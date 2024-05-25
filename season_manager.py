import random
import concurrent.futures
import time

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

def schedule_season_v2():
    num_teams = 30
    
    # Define conferences and divisions
    conferences = ['Conference 1', 'Conference 2']
    divisions = {'Conference 1': ['Division 1', 'Division 2', 'Division 3'],
                 'Conference 2': ['Division 4', 'Division 5', 'Division 6']}
    
    # Create a list of team ids
    teams = list(range(1, num_teams + 1))
    
    # Create dictionaries to store the schedule
    schedule = {team: [] for team in teams}
    
    def schedule_divisional_games(conference, division):
        teams_in_division = [team for team in teams if team % 3 == 1]
        for i, team in enumerate(teams_in_division):
            for opp_team in teams_in_division[i+1:]:
                for _ in range(4):
                    schedule[team].append(opp_team)
                    schedule[opp_team].append(team)
    
    def schedule_intra_conference_games(conference):
        other_teams = [team for team in teams if team % 3 != 1]
        for i, team in enumerate(teams):
            if team % 3 == 1:
                continue
            for _ in range(6):
                opp_team = random.choice(other_teams)
                while len(schedule[team]) - schedule[team].count(opp_team) >= 10:
                    opp_team = random.choice(other_teams)
                schedule[team].append(opp_team)
                schedule[opp_team].append(team)
            
            for _ in range(4):
                opp_team = random.choice(other_teams)
                while len(schedule[team]) - schedule[team].count(opp_team) >= 10 or schedule[team].count(opp_team) == 3:
                    opp_team = random.choice(other_teams)
                schedule[team].append(opp_team)
                schedule[opp_team].append(team)
    
    def schedule_inter_conference_games(team):
        other_teams = [t for t in teams if t != team]
        for _ in range(2):
            opp_team = random.choice(other_teams)
            schedule[team].append(opp_team)
            schedule[opp_team].append(team)
    
    print("Scheduling divisional games...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(schedule_divisional_games, conferences, divisions.values())
    
    print("Scheduling intra-conference games...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(schedule_intra_conference_games, conferences)
    
    print("Scheduling inter-conference games...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(schedule_inter_conference_games, teams)
    
    return schedule

def run_schedule_with_timeout():
    start_time = time.time()  # Capture the start time
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(schedule_season_v2)
        try:
            result = future.result(timeout=3600)  # Set timeout to 3600 seconds (1 hour)
        except concurrent.futures.TimeoutError:
            print("The scheduling process took too long and was terminated.")
            executor.shutdown(wait=False)
            return None
    end_time = time.time()  # Capture the end time
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    if result:
        print(f"The scheduling process completed successfully in {elapsed_time:.2f} seconds.")
    return result
    

def print_game_counts(home_schedule, away_schedule):
    print("Team\tHome Games\tAway Games")
    for team in home_schedule:
        home_games = len(home_schedule[team])
        away_games = len(away_schedule[team])
        print(f"{team}\t{home_games}\t\t{away_games}")



def schedule_season_v3(db_name):
    print('schedule_season_v3 called')

    


#For testing
# num_games = 82
# num_teams = 30
# host_limit = 12
# home_schedule, away_schedule = schedule_season_v1(num_games, num_teams, host_limit)
# print("Home Schedule:", home_schedule)
# print("Away Schedule:", away_schedule)

#print_game_counts(home_schedule, away_schedule)


# Run the scheduling function with a timeout
# schedule = run_schedule_with_timeout()
# if schedule:
#     for team, games in schedule.items():
#         print(f"Team {team}: {games}")