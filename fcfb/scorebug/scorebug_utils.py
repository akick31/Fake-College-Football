import sys
import os
import json

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


def get_scorebug_colors(home_team, away_team):
    """
    Make the scorebug colors visually different, compare the two primary colors via their hex code

    :param home_team:
    :param away_team:
    :return:
    """

    home_color = get_primary_color(home_team)
    away_color = get_primary_color(away_team)

    color_comparison = compare_color(home_color, away_color)

    # Try to get secondary colors
    if not color_comparison:
        home_color = get_secondary_color(home_team)
        away_color = get_secondary_color(away_team)
        color_comparison = compare_color(home_color, away_color)
        if not color_comparison:
            home_color = get_primary_color(home_team)
            away_color = get_secondary_color(away_team)
            color_comparison = compare_color(home_color, away_color)
            if not color_comparison:
                home_color = get_secondary_color(home_team)
                away_color = get_primary_color(away_team)
                color_comparison = compare_color(home_color, away_color)
                if not color_comparison:
                    color_comparison = {'home_color': "#000000", 'away_color': "#FF0000"}

    return {1: color_comparison['home_color'], 2: color_comparison['away_color']}


def compare_color(home_color, away_color):
    """
    Compare team colors and if they're within a threshold, use black and red

    :param home_color:
    :param away_color:
    :return:
    """

    if home_color != "#000000" and home_color is not None:
        home_hex = home_color.split("#")[1]
    else:
        home_hex = "000000"
    if away_color != "#000000" and away_color is not None:
        away_hex = away_color.split("#")[1]
    else:
        away_hex = "000000"

    home_decimal = int(home_hex, 16)
    away_decimal = int(away_hex, 16)

    # If difference is greater than 330000 they are far enough apart
    if abs(home_decimal - away_decimal) > 330000:
        return {'home_color': home_color, 'away_color': away_color}
    else:
        return False


def shorten_team_name(team):
    """
    Shorten the team name so it fits on the scorebug
    :param team:
    :return:
    """

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    with open(main_dir + '/fcfb/scorebug/shortened_names.json', 'r') as config_file:
        shortened_names_data = json.load(config_file)

    team = team.upper()
    if "STATE" in team:
        team = team.replace('STATE', 'ST')
    if team in shortened_names_data:
        team = shortened_names_data[team]

    return team
