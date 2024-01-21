import random
import csv
from names import first_names, last_names, nick_names

class Player:
    def __init__(self, player_id, first_name, last_name, nick_name, position, player_level, overall_score, player_salary, attributes):
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name
        self.nick_name = nick_name
        self.position = position
        self.player_level = player_level
        self.overall_score = overall_score
        self.player_salary = player_salary
        self.attributes = attributes

def assign_position(random_number):
    if random_number <= 15:
        return 'Center'
    elif 16 <= random_number <= 36:
        return 'Small Forward'
    elif 37 <= random_number <= 50:
        return 'Power Forward'
    elif 51 <= random_number <= 75:
        return 'Shooting Guard'
    else:
        return 'Point Guard'

def generate_player_attributes(player_level):
    # Determine overall score based on player level
    if player_level == 'Superstar':
        overall_score = random.randint(48, 60)
    elif player_level == 'All-Star':
        overall_score = random.randint(36, 47)
    elif player_level == 'Starter':
        overall_score = random.randint(24, 35)
    elif player_level == 'Role-Player':
        overall_score = random.randint(12, 23)
    else:  # 'Rookie'
        overall_score = random.randint(12, 40)

    # Generate random traits until their sum matches the overall score
    traits = {
        'strength': 2,
        'dexterity': 2,
        'constitution': 2,
        'intelligence': 2,
        'shooting': 2,
        'defense': 2,
    }

    while sum(traits.values()) != overall_score:
        # Randomly select a trait to increment
        trait_to_increment = random.choice(list(traits.keys()))
        # Increment the selected trait by 1
        traits[trait_to_increment] += 1

    return traits

def assign_player_level(random_number):
    if 1 <= random_number <= 3:
        return 'Superstar'
    elif 4 <= random_number <= 14:
        return 'All-Star'
    elif 15 <= random_number <= 45:
        return 'Starter'
    elif 46 <= random_number <= 91:
        return 'Role-Player'
    else:
        return 'Rookie'
    
def generate_salary(player_level):
    if player_level == 'Superstar':
        return random.randint(20, 40)
    elif player_level == 'All-Star':
        return random.randint(10, 30)
    elif player_level == 'Starter':
        return random.randint(8, 13)
    elif player_level == 'Role-Player':
        return random.randint(1, 9)
    else:  # 'Rookie'
        return random.randint(2, 7)

def generate_roster(num_players, type):
    roster = []

    for player_num in range(1, num_players + 1):
        player_id = player_num
        first_name = f'{random.choice(first_names)}'
        last_name = f'{random.choice(last_names)}'
        random_number_level = random.randint(1, 100)
        if type == 'rookies':
            player_level = 'Rookie'
        else:
            player_level = assign_player_level(random_number_level)
        random_number_position = random.randint(1, 100)
        position = assign_position(random_number_position)
        attributes = generate_player_attributes(player_level)
        overall_score = sum(attributes.values())
        player_salary = generate_salary(player_level)
        nick_name_number = random.randint(1, 250)
        if nick_name_number > 247:
            nick_name = f'"{random.choice(nick_names)}" '
        else: nick_name = ""
        player = Player(player_id, first_name, last_name, nick_name, position, player_level, overall_score, player_salary, attributes)
        roster.append(player)

    return roster

def display_roster(roster):
    for player in roster:
        print(f" #{player.player_id} - {player.first_name} {player.nick_name}{player.last_name} - {player.position} - {player.player_level} - Overall Level: {player.overall_score} - {player.player_salary}% Salary Cap Hit")
        print("Attributes:", player.attributes)
        print()

def display_totals(roster):
    total_salary = sum(player.player_salary for player in roster)
    print(f"Total Salary: {total_salary}")

    # Calculate sum of players by position
    players_by_position = {}
    for player in roster:
        if player.position in players_by_position:
            players_by_position[player.position] += 1
        else:
            players_by_position[player.position] = 1

    print("Players by Position:")
    for position, count in players_by_position.items():
        print(f"{position}: {count} players")


    players_by_level = {}
    for player in roster:
        if player.player_level in players_by_level:
            players_by_level[player.player_level] += 1
        else:
            players_by_level[player.player_level] = 1

    print("Players by Level:")
    for player_level, count in players_by_level.items():
        print(f"{player_level}: {count} players")


    # Calculate average overall level
    average_overall_level = sum(player.overall_score for player in roster) / len(roster)
    print(f"Average Overall Level: {average_overall_level}")

    total_salary = sum(player.player_salary for player in roster)
    print(f"Total Salary: {total_salary}")

    # Calculate average salary
    average_salary = sum(player.player_salary for player in roster) / len(roster)
    print(f"Average Salary: {average_salary}")

def export_to_csv(roster):
    csv_columns = ['Player_ID', 'First_Name', 'Last_Name', 'Nick_Name', 'Position', 'Player_Level', 'Overall_Score', 'Player_Salary']
    csv_file = "test_roster.csv"
    
    try:
        with open(csv_file, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for player in roster:
                writer.writerow({
                    'Player_ID': player.player_id,
                    'First_Name': player.first_name,
                    'Last_Name': player.last_name,
                    'Nick_Name': player.nick_name,
                    'Position': player.position,
                    'Player_Level': player.player_level,
                    'Overall_Score': player.overall_score,
                    'Player_Salary': player.player_salary
                })
        print(f"\nRoster data exported to {csv_file}")
    except Exception as e:
        print("Error writing to CSV:", e)

#for testing:
roster = generate_roster(100, 'rookies')
display_totals(roster)
#export_to_csv(roster)