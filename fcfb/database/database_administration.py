import tracemalloc
from datetime import datetime
import json
import mysql
import mysql.connector
import sys
import os

# getting the name of the directory
# where the this file is present.
from fcfb.database.check_database import check_if_game_exists_in_games
from fcfb.database.insert_into_database import insert_into_games
from fcfb.reddit_functions.parse_game_thread_info import get_game_info
from fcfb.reddit_functions.reddit_games import parse_game_id, insert_into_ongoing_games, \
    check_if_game_exists_in_ongoing_games
from fcfb.scorebug.scorebug_drawer import draw_ongoing_scorebug

current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from fcfb.logs.logs import *
from fcfb.maintain_functions.maintain_game_information import maintain_game_information


async def database_bot(r):
    """
    Run the database maintainer portion of Cyclone Bot

    :param r:
    :return:
    """

    while True:
        from fcfb.reddit_functions.reddit_games import add_games_from_wiki
        await add_games_from_wiki(r, "FakeCollegeFootball")
        await maintain_game_information(r)


def connect_to_database():
    """
    Connect to the FCFB database

    """

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    with open(main_dir + '/configuration/database_config.json', 'r') as config_file:
        config_data = json.load(config_file)

    database = mysql.connector.connect(
        host=config_data['database_host'],
        user=config_data['database_user'],
        passwd=config_data['database_password'],
        database=config_data['database'],
    )

    if database.is_connected():
        log_message("database", "info", "Connected to the FCFB Database")
    else:
        log_message("database", "error", "Could not connect to the FCFB Database")
        return

    return database


def add_game_to_databases(r, game, season, subdivision):
    if "link" in game:
        game_link = game.split(")|[rerun]")[0].split("[link](")[1]
        game_link_id = game_link.split("/comments")[1]

        submission = r.submission(game_link_id)
        submission_body = submission.selftext

        game_thread_timestamp = datetime.fromtimestamp(submission.created)

        game_id = parse_game_id(submission_body)

        # If the game doesn't exist, parse the info add it to the database
        if game_id is not None and not check_if_game_exists_in_games(game_id):
            game_info = get_game_info(game_id, submission, subdivision)

            is_final = 1
            if "Game complete" not in submission_body or "Unable to generate play list" in submission_body:
                is_final = 0

            insert_into_games(game_id, game_link, game_info, season, is_final, game_thread_timestamp)

        if ("Game complete" not in submission_body or "Unable to generate play list" in submission_body)\
                and game_id is not None and not check_if_game_exists_in_ongoing_games(game_id):
            game_info = get_game_info(game_id, submission, subdivision)
            draw_ongoing_scorebug(game_id, game_info['quarter'], game_info['clock'],
                                  game_info['down_and_distance'],
                                  game_info['possession'],
                                  game_info['home_team'], game_info['away_team'], game_info['home_score'],
                                  game_info['away_score'],
                                  game_info['team_with_possession'], game_info['home_record'],
                                  game_info['away_record'])
            insert_into_ongoing_games(game_id, game_link, game_info)
