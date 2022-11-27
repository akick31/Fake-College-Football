import sys
import os

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from fcfb.database.retrieve_from_database import *


def get_vegas_odds(home_team, away_team, database):
    """
    Return a dictionary containing the vegas odds for the game

    """

    home_elo = get_elo(home_team)
    away_elo = get_elo(away_team)
    if home_elo is None or away_elo is None:
        return None

    home_odds = calculate_vegas_odds(home_elo, away_elo)
    away_odds = calculate_vegas_odds(away_elo, home_elo)
    # Default to a push if can't find Elo
    if home_elo == -500 or away_elo == -500:
        home_odds = 0
        away_odds = 0
    return {1: home_odds, 2: away_odds}


def calculate_vegas_odds(team_elo, opponent_elo):
    """
    Calculate Vegas odds using a constant and team and their opponent Elo

    """

    constant = 18.14010981807
    odds = (float(opponent_elo) - float(team_elo))/constant
    return odds
