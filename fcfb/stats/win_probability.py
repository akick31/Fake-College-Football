import math
import xgboost as xgb
import pandas as pd
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

from database.retrieve_from_database import *

data = {
  'down': [4],
  'distance': [4],
  'position': [38],
  'margin': [17],
  'seconds_left_game': [350],
  'seconds_left_half': [350],
  'half': [2],
  'had_first_possession': [1],
  'elo_diff_time': [27.0449]
}


def get_current_win_probability(possession, home_team, away_team, home_score, away_score, quarter, clock, ball_location, down, yards_to_go, actual_result, had_first_possession):
    """
    Get the current win probability for the line you are on in the gist

    :param possession:
    :param home_team:
    :param away_team:
    :param home_score:
    :param away_score:
    :param quarter:
    :param clock:
    :param ball_location:
    :param down:
    :param yards_to_go:
    :param actual_result:
    :param had_first_possession:
    :return:
    """

    if possession == "home":
        offense_score = home_score
        defense_score = away_score
    elif possession == "away":
        offense_score = away_score
        defense_score = home_score
    elif possession == "home" and str(actual_result) == "TOUCHDOWN":
        offense_score = str(int(home_score) + 6)
        defense_score = away_score
    elif possession == "away" and str(actual_result) == "TOUCHDOWN":
        offense_score = str(int(away_score) + 6)
        defense_score = home_score
    elif possession == "home" and str(actual_result) == "TURNOVER_TOUCHDOWN":
        offense_score = str(int(away_score) + 6)
        defense_score = home_score
    elif possession == "away" and str(actual_result) == "TURNOVER_TOUCHDOWN":
        offense_score = str(int(home_score) + 6)
        defense_score = away_score
    elif possession == "home" and str(actual_result) == "PAT":
        offense_score = str(int(home_score) + 1)
        defense_score = away_score
    elif possession == "away" and str(actual_result) == "PAT":
        offense_score = str(int(away_score) + 1)
        defense_score = home_score
    elif possession == "home" and str(actual_result) == "TWO_POINT":
        offense_score = str(int(home_score) + 2)
        defense_score = away_score
    elif possession == "away" and str(actual_result) == "TWO_POINT":
        offense_score = str(int(away_score) + 2)
        defense_score = home_score
    margin = int(offense_score) - int(defense_score)

    # get seconds left in half and seconds left in game and current half
    if quarter == "1":
        seconds_left_game = 1680-(420-int(clock))
        seconds_left_half = 840-(420-int(clock))
        half = 1
    elif quarter == "2":
        seconds_left_game = 1260-(420-int(clock))
        seconds_left_half = 420-(420-int(clock))
        half = 1
    elif quarter == "3":
        seconds_left_game = 840-(420-int(clock))
        seconds_left_half = 840-(420-int(clock))
        half = 2
    elif quarter == "4":
        seconds_left_game = 420-(420-int(clock))
        seconds_left_half = 420-(420-int(clock))
        half = 2
    else:
        seconds_left_game = 0
        seconds_left_half = 0
        half = 2

    position = 100-int(ball_location)
    down = int(down)
    distance = int(yards_to_go)

    home_elo = get_elo(home_team)
    away_elo = get_elo(away_team)

    if home_elo is None:
        home_elo = 500
    elif away_elo is None:
        away_elo = 500

    # get elo
    if possession == "home":
        offense_elo = home_elo
        defense_elo = away_elo
    else:
        offense_elo = away_elo
        defense_elo = home_elo

    elo_diff_time = (float(offense_elo) - float(defense_elo)) * math.exp(-2 * (1 - (seconds_left_game / 1680)))

    # Set all the data in the dictionary
    # If the home team has the ball on line 1, it means they kicked it off and deferred
    data["had_first_possession"] = [had_first_possession]
    data["margin"] = [margin]
    data["down"] = [down]
    data["distance"] = [distance]
    data["position"] = [position]
    data["seconds_left_game"] = [seconds_left_game]
    data["seconds_left_half"] = [seconds_left_half]
    data["half"] = [half]
    data["elo_diff_time"] = [elo_diff_time]

    return calculate_win_probability(data)


def calculate_win_probability(data):
    """
    Using the model, calculate the current win probability

    :param data:
    :return:
    """

    model_xgb = xgb.XGBRegressor()

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    model_xgb.load_model(main_dir + '/machine_learning/wpmodel.json')

    df_data = pd.DataFrame.from_dict(data)
    win_probability = model_xgb.predict(df_data)

    return float(win_probability)*100