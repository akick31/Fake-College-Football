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


def insert_into_ongoing_games(game_id, game_link, game_info):
    """
    Insert the game into the ongoing games database

    :param game_id:
    :param game_link:
    :param game_info:
    :return:
    """

    try:
        log_message("database", "info", "----------------------------")
        log_message("database", "info", "Inserting game info for " + game_id + " into the ongoing games database")
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("INSERT INTO ongoing_games (game_id, home_team, away_team, home_coach, away_coach, "
                       "home_offensive_playbook, away_offensive_playbook, home_defensive_playbook, away_defensive_playbook, "
                       "home_score, away_score, possession, quarter, clock, ball_location, down, yards_to_go, "
                       "tv_channel, game_link, subdivision, scorebug) VALUES ("
                        + "'" + game_id + "', "
                        + "'" + game_info['home_team'] + "', "
                        + "'" + game_info['away_team'] + "', "
                        + "'" + game_info['home_coach'] + "', "
                        + "'" + game_info['away_coach'] + "', "
                        + "'" + game_info['home_offensive_playbook'] + "', "
                        + "'" + game_info['away_offensive_playbook'] + "', "
                        + "'" + game_info['home_defensive_playbook'] + "', "
                        + "'" + game_info['away_defensive_playbook'] + "', "
                        + game_info['home_score'] + ", "
                        + game_info['away_score'] + ", "
                        + "'" + game_info['possession'] + "', "
                        + game_info['quarter'] + ", "
                        + "'" + game_info['clock'] + "', "
                        + "'" + game_info['ball_location'] + "', "
                        + "'" + game_info['down'] + "', "
                        + game_info['yards_to_go'] + ", "
                        + "'" + game_info['tv_channel'] + "', "
                        + "'" + game_link + "', "
                        + "'" + game_info['subdivision'] + "', "
                        + "'" + game_info['scorebug'] + "')")
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


def insert_into_games(game_id, game_link, game_info, season, is_final, game_thread_timestamp):
    """
    Insert the game into the games database

    :param game_id:
    :param game_link:
    :param game_info:
    :param season:
    :param is_final:
    :param game_thread_timestamp:
    :return:
    """

    try:
        log_message("database", "info", "----------------------------")
        log_message("database", "info", "Inserting game info for " + game_id + " into the games database")
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("INSERT INTO games (game_id, home_team, away_team, start_time, location, tv_channel, home_coach, "
                       "away_coach, home_offensive_playbook, away_offensive_playbook, home_defensive_playbook, "
                       "away_defensive_playbook, game_thread_timestamp, subdivision, home_score, away_score, "
                       "game_link, is_final, season, scorebug) VALUES ("
                        + "'" + game_id + "', "
                        + "'" + game_info['home_team'] + "', "
                        + "'" + game_info['away_team'] + "', "
                        + "'" + game_info['start_time'] + "', "
                        + "'" + game_info['location'] + "', "
                        + "'" + game_info['tv_channel'] + "', "
                        + "'" + game_info['home_coach'] + "', "
                        + "'" + game_info['away_coach'] + "', "
                        + "'" + game_info['home_offensive_playbook'] + "', "
                        + "'" + game_info['away_offensive_playbook'] + "', "
                        + "'" + game_info['home_defensive_playbook'] + "', "
                        + "'" + game_info['away_defensive_playbook'] + "', "
                        + "'" + str(game_thread_timestamp) + "', "
                        + "'" + game_info['subdivision'] + "', "
                        + game_info['home_score'] + ", "
                        + game_info['away_score'] + ", "
                        + "'" + game_link + "', "
                        + "'" + str(is_final) + "', "
                        + str(season) + ", "
                        + "'" + game_info['scorebug'] + "')")
        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Successfully inserted game info for " + game_id + " into the games database")
        log_message("database", "info", "Database disconnected")
        return True
    except Exception as e:
        log_message("database", "error", "There was an issue inserting the game info for " + game_id + " into the games database. " + repr(e))
        log_message("database", "info", "Database disconnected")
        return False


def insert_play(game_id, home_team, away_team, play_number, home_score, away_score, game_quarter, clock,
                ball_location, possession, down, yards_to_go, defensive_number, offensive_number, defensive_submitter,
                offensive_submitter, play, result, actual_result, yards, play_time, runoff_time, win_probability):
    """
    Insert play into database

    :param game_id:
    :param home_team:
    :param away_team:
    :param play_number:
    :param home_score:
    :param away_score:
    :param game_quarter:
    :param clock:
    :param ball_location:
    :param possession:
    :param down:
    :param yards_to_go:
    :param defensive_number:
    :param offensive_number:
    :param defensive_submitter:
    :param offensive_submitter:
    :param play:
    :param result:
    :param actual_result:
    :param yards:
    :param play_time:
    :param runoff_time:
    :param win_probability:
    :return:
    """

    try:
        log_message("database", "info", "----------------------------")
        log_message("database", "info", "Inserting play info for " + game_id + ". Play number " + str(play_number))
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute(
            "INSERT INTO game_plays (game_id, home_team, away_team, play_number,home_score,away_score,game_quarter,clock,ball_location,possession,down,yards_to_go,defensive_number,offensive_number,defensive_submitter,offensive_submitter,play,result,actual_result,yards,play_time,runoff_time,win_probability) VALUES ("
            + "'" + str(game_id) + "', "
            + "'" + str(home_team) + "', "
            + "'" + str(away_team) + "', "
            + str(play_number) + ", "
            + home_score + ", "
            + away_score + ", "
            + game_quarter + ", "
            + clock + ", "
            + ball_location + ", '"
            + possession + "', "
            + down + ", "
            + yards_to_go + ", "
            + defensive_number + ", "
            + offensive_number + ", '"
            + defensive_submitter + "', '"
            + offensive_submitter + "', '"
            + play + "', '"
            + result + "', '"
            + actual_result + "', "
            + yards + ", "
            + play_time + ", "
            + runoff_time + ", "
            + win_probability + ")")
        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Successfully inserted play info for " + game_id + ". Play number " + str(play_number))
        log_message("database", "info", "Database disconnected")
        return True

    except Exception as e:
        log_message("database", "error", "There was an issue inserting play info for " + game_id + ". Play number " + str(play_number) + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return False