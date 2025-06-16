# fastbreaks-and-cap-space

Run game_test_manager.py and players will be generated and automatically drafted to teams. Default values: 30 teams, 550 players, 150 salary cap.

Game simulation is currently barebones to work on testing trades/other features. Current work focus is adding a user interface and trade simulator.

Current features:

- Creates unique Players with 6 tabletop RPG inspired attributes + salary and position
- Creates unique Teams
- Drafts all players to Teams in a 15 round fantasy snake draft taking into account salary cap and team's current positional needs
- Simulates full 82-game season
- Simulates full playoffs with seeding and 2-2-1-1-1 home/away 7 game series (no play-in yet)
- Holds all data in star schema SQLite warehouse (ERD below)

In progress:
- UI for gameplay (Pygame)
- Trade Machine logic
- Rival GM AI logic


![fantasty_basketball_erd](https://github.com/user-attachments/assets/18b25b4e-67e3-4211-94f2-c998ea25954d)
