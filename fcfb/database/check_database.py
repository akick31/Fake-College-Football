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

from logs.logs import *


def check_if_game_exists(game_id):
    """
    Check if the game exists in the database already

    :param game_id:
    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Checking if the game " + game_id + " already exists")

    try:
        from database.database_administration import connect_to_database
        database = connect_to_database()
        cursor = database.cursor()
        cursor.execute("SELECT COUNT(1) FROM games WHERE (game_id) IN (('" + str(game_id) + "'))")
        game_exists = cursor.fetchone()[0]
        if game_exists >= 1:
            log_message("database", "info", "The game " + game_id + " exists already.")
            log_message("database", "info", "Database disconnected")
            return True
        else:
            log_message("database", "info", "The game " + game_id + " does not exist!")
            log_message("database", "info", "Database disconnected")
            return False
    except Exception as e:
        log_message("database", "error", "There was an issue checking if the game " + game_id + " already exists or not. " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def check_number_of_plays(game_id):
    """
    Get the number of plays in the game

    :param game_id:
    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Checking the number of plays in the following game: " + game_id)

    try:
        from database.database_administration import connect_to_database
        database = connect_to_database()
        cursor = database.cursor()
        cursor.execute("SELECT COUNT(*) FROM game_plays WHERE (game_id) IN (('" + str(game_id) + "'))")
        num_plays = cursor.fetchone()[0]

        log_message("database", "info", "The game " + game_id + " contains " + str(num_plays) + " plays")
        log_message("database", "info", "Database disconnected")
        return num_plays
    except Exception as e:
        log_message("database", "error", "There was an issue checking the number of plays in the following game: " + game_id + " " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def check_game_done(game_id):
    """
    Check if the game is marked as done

    :param game_id:
    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Checking the game " + game_id + " is marked as done")

    try:
        from database.database_administration import connect_to_database
        database = connect_to_database()
        cursor = database.cursor()
        cursor.execute("SELECT is_final FROM games WHERE (game_id) IN (('" + str(game_id) + "'))")
        is_done = cursor.fetchone()[0]

        log_message("database", "info", "The game status for " + game_id + " is marked as " + str(is_done))
        log_message("database", "info", "Database disconnected")
        return is_done
    except Exception as e:
        log_message("database", "error", "There was an issue checking the game " + game_id + " to see if it is marked as done. " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None
