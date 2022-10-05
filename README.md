# Fake College Football
A repository of all the bots that run and maintains various FCFB functions, such as the scoreboard, elo, and more

___
## Bots
### Cyclone Bot
#### Discord Scoreboard
Cyclone Bot will monitor the FCFB wiki and add ongoing games to the database. Once added to the database, Cyclone Bot will then add each ongoing game into a scoreboard channel with a scorebug in the Discord server and continuously monitor those games and update the scoreboard accordingly.  While Cyclone Bot does this, it also saves the play list into the database for future queries. 
#### Historical Results
Because Database Bot stores all of the games in the database and has access to said database, Cyclone Bot can then seamlessly and quickly pull historical results and their plots on request
___
### Database Bot
#### ELO
Database Bot will monitor FCFB and update ELO throughout the season for all teams accordingly. ELO is then used to calculate spread and used in win probability.

#### Statistics
As Database Bot monitors the ongoing FCFB games, it uploads statistics from each game to a database. These statistics will be visible to the public and available upon request
