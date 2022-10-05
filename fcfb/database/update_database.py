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

from database.database_administration import *
from logs.logs import *


def update_ongoing_games(game_id, game_info):
    """
    Update the game in the ongoing games database

    :param game_id:
    :param game_info:
    :return:
    """

    try:
        log_message("database", "info", "----------------------------")
        log_message("database", "info", "Updating the game info for " + game_id + " into the ongoing games database")
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("UPDATE ongoing_games SET "
                        + "home_score = " + game_info['home_score'] + ", "
                        + "away_score = " + game_info['away_score'] + ", "
                        + "possession = '" + game_info['possession'] + "', "
                        + "quarter = " + game_info['quarter'] + ", "
                        + "clock = '" + game_info['clock'] + "', "
                        + "ball_location = " + game_info['ball_location'] + ", "
                        + "down = " + game_info['down'] + " WHERE (game_id) IN (('" + game_id + "'))")
        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Successfully inserted game info for " + game_id + " into the ongoing games database")
        log_message("database", "info", "Database disconnected")
        return True
    except Exception as e:
        log_message("database", "error", "There was an issue inserting the game info for " + game_id + " into the ongoing games database. " + repr(e))
        log_message("database", "info", "Database disconnected")
        return False


def update_discord_comment_id_into_ongoing_games(game_id, discord_comment_id):
    """
    Update the comment id in the ongoing games database

    :param game_id:
    :param discord_comment_id:
    :return:
    """

    try:
        log_message("database", "info", "----------------------------")
        log_message("database", "info", "Updating the discord comment id for " + game_id + " into the ongoing games database")
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("UPDATE ongoing_games SET "
                        + "discord_comment_id = '" + str(discord_comment_id) + "' WHERE (game_id) IN (('" + game_id + "'))")
        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Successfully updated discord comment id for " + game_id + " into the ongoing games database")
        log_message("database", "info", "Database disconnected")
        return True
    except Exception as e:
        log_message("database", "error", "There was an issue updating the discord comment id for " + game_id + " into the ongoing games database. " + repr(e))
        log_message("database", "info", "Database disconnected")
        return False


def update_win_probability(game_id, win_probability):
    """
    Update win probability in the ongoing games database

    :param game_id:
    :param win_probability:
    :return:
    """

    try:
        log_message("database", "info", "----------------------------")
        log_message("database", "info", "Updating win probability for " + game_id + " in the ongoing games database.")
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("UPDATE ongoing_games SET "
                       + "win_probability = " + str(win_probability) + " "
                       + "WHERE (game_id) IN (('" + game_id + "'))")
        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info",
                    "Successfully updated win probability for " + game_id + " in the ongoing games database")
        log_message("database", "info", "Database disconnected")
        return True

    except Exception as e:
        log_message("database", "error", "There was an issue updating the win probability for " + game_id + " in the ongoing games database. " + repr(e))
        log_message("database", "info", "Database disconnected")
        return False


def mark_game_done(game_id):
    """
    Mark the game as done in the games database

    :param game_id:
    :return:
    """

    try:
        log_message("database", "info", "----------------------------")
        log_message("database", "info", "Marking game " + game_id + " as done.")
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("UPDATE games SET "
                       + "is_final = '1' "
                       + "WHERE (game_id) IN (('" + game_id + "'))")
        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info",
                    "Successfully marked game " + game_id + " as done")
        log_message("database", "info", "Database disconnected")
        return True

    except Exception as e:
        log_message("database", "error", "There was an issue marking " + game_id + " as done. " + repr(e))
        log_message("database", "info", "Database disconnected")
        return False
