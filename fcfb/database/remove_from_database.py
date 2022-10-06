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


def remove_game_from_ongoing_games(game_id):
    """
    Remove the game from the ongoing game database

    :param game_id:
    :return:
    """

    log_message("database", "info", "Trying to remove game " + game_id + " from the ongoing games database")
    try:
        from database.database_administration import connect_to_database
        database = connect_to_database()
        cursor = database.cursor()
        cursor.execute("DELETE FROM ongoing_games WHERE (game_id) IN (('" + game_id + "'))")
        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Removed game " + game_id + " from ongoing games database")
        return True
    except Exception as e:
        log_message("database", "error", "Error removing game " + game_id + " from the ongoing games database. " + repr(e))
        return None
