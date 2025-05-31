#Initial test to sim a starting draft
import data_manager
import game_data_manager
import csv
import player_generator
import team_generator
import draft_manager
import names
import season_manager

starting_year = 2025

league_db_name = "league01.db"

salary_cap = 150

def create_players_and_teams(league_db_name, player_count, team_count):
    
    #Clear out any existing tables

    #Drop player table
    data_manager.drop_table(league_db_name, "dim_players")
    #Drop teams table
    data_manager.drop_table(league_db_name, "dim_teams")
    #Drop draft list
    data_manager.drop_table(league_db_name, "fact_drafted_players")
    #Drop teams rosters
    data_manager.drop_table(league_db_name, "fact_team_rosters")
    #Drop schedule
    data_manager.drop_table(league_db_name, "fact_season_schedule")
    #Drop conferneces and divisions
    data_manager.drop_table(league_db_name, "fact_conferences_divisions")
    #Drop player transaction table
    data_manager.drop_table(league_db_name, "dim_player_transactions")
    #Drop game results table
    data_manager.drop_table(league_db_name, "fact_game_results")


    #Create players and teams

    #Create players - second argurment as 'rookies' creates a rookie class, any other value produces all player classes
    players = player_generator.generate_roster(player_count, 'normal')
    #Create player dimension table and load players into it
    data_manager.create_player_table(league_db_name, players)
    #Create conferences and divisions
    conferences_and_divisions = names.conferences_and_divisions
    data_manager.create_conferences_and_divsions_table(league_db_name, conferences_and_divisions)
    #Create teams
    teams = team_generator.generate_teams(team_count)
    #Create team dimension table and load teams into it
    data_manager.create_team_table(league_db_name, teams)
    #Create player transaction table
    data_manager.create_player_transaction_table(league_db_name)
    #Create game results table
    game_data_manager.create_fact_game_results(league_db_name)
    
#Assign players to all teams 
def initial_draft(league_db_name, salary_cap, starting_year):
    data_manager.create_draft_table(league_db_name)
    draft_manager.snake_draft_players_for_all_teams(league_db_name, salary_cap, starting_year)

def create_season_schedule(league_db_name, season_number):
    
    with open('schedule _output.csv','r') as csv_schedule:
        #Skip header line
        csv_schedule.__next__()
        schedule=[tuple(row) for row in csv.reader(csv_schedule)]
        #schedule_dict = csv.DictReader(csv_schedule) # comma is default delimiter
        #schedule = [(i['Away'], i['Home'], i['Day']) for i in schedule_dict]

    data_manager.create_season_schedule(league_db_name, season_number, schedule)

def game_init(league_db_name, salary_cap, starting_year):
    #Step 0 - Create a league with 550 players and 30 teams
    create_players_and_teams(league_db_name, 550, 30)

    #Step 1 - Draft the players to all 30 teams
    initial_draft(league_db_name, salary_cap, starting_year)

    #Step 2 - Create the season schedule where 2025 is the season number (first season)
    create_season_schedule(league_db_name, starting_year)
    

def run_multi_seasons(league_db_name, salary_cap, starting_year, season_count):
    
    game_init(league_db_name, salary_cap, starting_year)

    seasons_run = 0
    current_season = starting_year

    while seasons_run < season_count:

        season_manager.run_season_schedule(league_db_name, current_season)

        season_manager.create_standings_view(league_db_name)
 

        winner = season_manager.run_post_season("league01.db", current_season)


        print("Winning Team is", winner)

        current_season = current_season + 1

        create_season_schedule(league_db_name, current_season)

        seasons_run = seasons_run + 1





def run_single_season(league_db_name, salary_cap, starting_year):
    #Start game with default salary_cap (150)]

    game_init(league_db_name, salary_cap, starting_year)

    season_manager.run_season_schedule(league_db_name, starting_year)

    season_manager.create_standings_view(league_db_name)

    winner = season_manager.run_post_season("league01.db", starting_year)


    print("Winning Team is", winner)


#run_single_season(league_db_name, salary_cap, starting_year)

season_count = 100
run_multi_seasons(league_db_name, salary_cap, starting_year, season_count)






