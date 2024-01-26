import random
from names import locations

class Team:
    def __init__(self, team_id, location_name, team_name):
        self.player_id = team_id
        self.location_name = location_name
        self.team_name = team_name



def select_unique_entry(my_list, selected_entries):
    remaining_entries = list(set(my_list) - set(selected_entries))
    
    if not remaining_entries:
        print("All entries have been selected.")
        return None
    
    selected_entry = random.choice(remaining_entries)
    selected_entries.append(selected_entry)
    
    return selected_entry

# Example usage:
selected_entries = []

# Select entries until all are selected
while True:
    entry = select_unique_entry(locations, selected_entries)
    if entry is None:
        break
    print(f"Selected entry: {entry}")

