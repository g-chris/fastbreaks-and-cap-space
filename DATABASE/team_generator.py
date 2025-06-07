import random
from DATABASE.names import locations, team_names

class Team:
    def __init__(self, team_id, location_name, team_name, conf_div_id):
        self.team_id = team_id
        self.location_name = location_name
        self.team_name = team_name
        self.conf_div_id = conf_div_id

selected_locations = []
selected_team_names = []

def select_unique_entry(my_list, selected_entries):
    remaining_entries = [entry for entry in my_list if entry not in selected_entries]

    if not remaining_entries:
        #print("All entries have been selected.")
        return None
    
    selected_entry = random.choice(remaining_entries)
    selected_entries.append(selected_entry)
    
    return selected_entry

def pick_location():

    # Select entries until all are selected
    while True:
        entry = select_unique_entry(locations, selected_locations)
        if entry is None:
            break
        #print(f"Selected entry: {entry}")

        return entry



def pick_team_name():

    # Select entries until all are selected
    while True:
        entry = select_unique_entry(team_names, selected_team_names)
        if entry is None:
            break
        #print(f"Selected entry: {entry}")

        return entry

# def add_conf_div(team_num):
#     if team_num % 2 != 0:
#         return (team_num // 2) % 3 + 4  # Cycle through 4, 5, 6
#     else:
#         return (team_num // 2) % 3 + 1  # Cycle through 1, 2, 3

def add_conf_div(team_num):
    if team_num <= 5:
        return(1)
    if team_num <= 10:
        return(2)
    if team_num <=15:
        return(3)
    if team_num <= 20:
        return(4)
    if team_num <= 25:
        return(5)
    else:
        return(6)  
def generate_teams(num_teams):
    teams = []

    for team_num in range(1, num_teams + 1):
        team_id = team_num
        location_name = pick_location()
        team_name = pick_team_name()
        conf_div_id = add_conf_div(team_num)
        team = Team(team_id, location_name, team_name, conf_div_id)
        teams.append(team)
    return teams
        
def print_teams(teams):
    for team in teams:
        print(f" #{team.team_id} - {team.location_name} {team.team_name} {team.conf_div_id}")

#For testing
#teams = generate_teams(30)
#print_teams(teams)
