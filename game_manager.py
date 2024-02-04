#Initial test to sim a starting draft
import data_manager
import player_generator
import team_generator
import draft_manager



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

    #Create players and teams

    #Create players - second argurment as 'rookies' creates a rookie class, any other value produces all palyer classes
    players = player_generator.generate_roster(player_count, 'normal')
    #Create player dimension table and load players into it
    data_manager.create_player_table(league_db_name, players)
    #Create teams
    teams = team_generator.generate_teams(team_count)
    #Create team dimension table and load teams into it
    data_manager.create_team_table(league_db_name, teams)

#Assign players to all teams 
def initial_draft(league_db_name, salary_cap):
    data_manager.create_draft_table(league_db_name)
    draft_manager.snake_draft_players_for_all_teams(league_db_name, salary_cap)
    #data_manager.print_draft_table(league_db_name)


#print('create players and teams')
create_players_and_teams("league01.db", 550, 30)

salary_cap = 150

initial_draft("league01.db", salary_cap)

#data_manager.print_team_table("league01.db")

#data_manager.print_player_table("league01.db")











