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

from fcfb.logs.logs import *


def get_elo(team):
    """
    Get the current ELO for the team called

    :param team:
    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Retrieving the ELO for " + team)
    try:
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return False

        cursor = database.cursor()
        cursor.execute("SELECT ELO FROM elo WHERE team = '" + team + "'")
        team_elo = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Retrieved ELO for " + team + ". ELO is " + str(team_elo))
        log_message("database", "info", "Database disconnected")
        return team_elo
    except Exception as e:
        log_message("database", "error", "There was an error retrieving ELO for " + team + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def get_primary_color(team):
    """
    Get the primary team color

    :param team:
    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Retrieving the primary team color for " + team)
    try:
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT primary_color FROM teams WHERE name = '" + team + "'")
        team_elo = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Retrieved primary team color for " + team + ". primary team color is " + str(team_elo))
        log_message("database", "info", "Database disconnected")
        return team_elo
    except Exception as e:
        log_message("database", "error", "There was an error retrieving primary team color for " + team + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def get_secondary_color(team):
    """
    Get the secondary team color

    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Retrieving the secondary team color for " + team)
    try:
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()

        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT secondary_color FROM teams WHERE name = '" + team + "'")
        team_elo = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Retrieved secondary team color for " + team + ". secondary team color is " + str(team_elo))
        log_message("database", "info", "Database disconnected")
        return team_elo
    except Exception as e:
        log_message("database", "error", "There was an error retrieving secondary team color for " + team + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def get_ongoing_game_id(game_link):
    """
    Fetch the game id for the ongoing game

    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Retrieving the game id for the ongoing game with the following url: " + game_link)
    try:
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT game_id FROM ongoing_games WHERE (game_link) IN (('" + game_link + "'))")
        game_id = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Retrieved the game id for the ongoing game with the following url: " + game_link)
        log_message("database", "info", "Database disconnected")
        return game_id
    except Exception as e:
        log_message("database", "error", "There was an error retrieving the game id for the ongoing game with the following url: " + game_link + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def get_ongoing_game_links():
    """
    Fetch the game link for all ongoing games

    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Retrieving the game thread links for ongoing games")
    try:
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT game_link FROM ongoing_games")
        game_links = cursor.fetchall()

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Retrieved the game thread links array for ongoing games")
        log_message("database", "info", "Database disconnected")
        return game_links
    except Exception as e:
        log_message("database", "error", "There was an error retrieving the ongoing game thread links. " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def get_ongoing_game_subdivision(game_id):
    """
    Fetch the game subdivision for the ongoing game

    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Retrieving the subdivision for the ongoing game with the following game id: " + game_id)
    try:
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT subdivision FROM ongoing_games WHERE (game_id) IN (('" + game_id + "'))")
        subdivision = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Retrieved the subdivision for the ongoing game with the following game id: " + game_id)
        log_message("database", "info", "Database disconnected")
        return subdivision
    except Exception as e:
        log_message("database", "error", "There was an error retrieving the subdivision for the ongoing game with the following game id: " + game_id + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def get_current_season():
    """
    Fetch the current ongoing season

    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Retrieving the current season")
    try:
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT season FROM seasons")
        season = cursor.fetchall()[-1][0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Retrieved the current season")
        log_message("database", "info", "Database disconnected")
        return season
    except Exception as e:
        log_message("database", "error", "There was an error retrieving the current season. " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def get_discord_comment_id(game_id):
    """
    Fetch the game subdivision for the ongoing game

    :param game_id:
    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Retrieving the discord comment id for the ongoing game with the following game id: " + game_id)
    try:
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT discord_comment_id FROM ongoing_games WHERE (game_id) IN (('" + game_id + "'))")
        discord_comment_id = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Retrieved the discord comment id for the ongoing game with the following game id: " + game_id)
        log_message("database", "info", "Database disconnected")
        return discord_comment_id
    except Exception as e:
        log_message("database", "error", "There was an error retrieving the discord comment id for the ongoing game with the following game id: " + game_id + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def get_win_probability(game_id):
    """
    Fetch the win probability for the ongoing game

    :param game_id:
    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Retrieving the win probability for the ongoing game with the following game id: " + game_id)
    try:
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT win_probability FROM ongoing_games WHERE (game_id) IN (('" + game_id + "'))")
        win_probability = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Retrieved the win probability for the ongoing game with the following game id: " + game_id)
        log_message("database", "info", "Database disconnected")
        return win_probability
    except Exception as e:
        log_message("database", "error", "There was an error retrieving the win probability for the ongoing game with the following game id: " + game_id + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def get_scorebug(game_id):
    """
    Fetch the scorebug for the ongoing game

    :param game_id:
    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Retrieving the scorebug for the ongoing game with the following game id: " + game_id)
    try:
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT scorebug FROM ongoing_games WHERE (game_id) IN (('" + game_id + "'))")
        scorebug = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Retrieved the scorebug for the ongoing game with the following game id: " + game_id)
        log_message("database", "info", "Database disconnected")
        return scorebug
    except Exception as e:
        log_message("database", "error", "There was an error retrieving the scorebug for the ongoing game with the following game id: " + game_id + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def get_game_plays_win_probability(game_id):
    """
    Fetch the latest win probability from the game plays database

    :param game_id:
    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Retrieving the win probability for the ongoing game with the following game id: " + game_id)
    try:
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT win_probability FROM game_plays WHERE (game_id) IN (('" + game_id + "'))")
        win_probability = cursor.fetchall()[-1][0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Retrieved the win probability for the ongoing game with the following game id: " + game_id)
        log_message("database", "info", "Database disconnected")
        return win_probability
    except Exception as e:
        log_message("database", "error", "There was an error retrieving the win probability for the ongoing game with the following game id: " + game_id + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def get_team_subdivision(team):
    """
    Fetch the team's subdivision

    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Retrieving the subdivision for the following team: " + team)
    try:
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT subdivision FROM teams WHERE (name) IN (('" + team + "'))")
        subdivision = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Retrieved the subdivision for the following team: " + team)
        log_message("database", "info", "Database disconnected")
        return subdivision
    except Exception as e:
        log_message("database", "error", "There was an error retrieving the subdivision for the following team: " + team + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def get_season_start(season):
    """
    Fetch the season start date

    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Retrieving the season start date for season " + str(season))
    try:
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT season_start FROM seasons WHERE (season) IN ((" + str(season) + "))")
        subdivision = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Retrieved the season start date for season " + str(season))
        log_message("database", "info", "Database disconnected")
        return subdivision
    except Exception as e:
        log_message("database", "error", "There was an error retrieving the season start date for season " + str(season) + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def get_season_end(season):
    """
    Fetch the season end date

    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Retrieving the season end date for season " + str(season))
    try:
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT season_end FROM seasons WHERE (season) IN ((" + str(season) + "))")
        subdivision = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Retrieved the season end date for season " + str(season))
        log_message("database", "info", "Database disconnected")
        return subdivision
    except Exception as e:
        log_message("database", "error", "There was an error retrieving the season end date for season " + str(season) + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def get_postseason_start(season):
    """
    Fetch the postseason start date

    :return:
    """

    log_message("database", "info", "----------------------------")
    log_message("database", "info", "Retrieving the postseason start date for season " + str(season))
    try:
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT postseason_start FROM seasons WHERE (season) IN ((" + str(season) + "))")
        subdivision = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info", "Retrieved the postseason start date for season " + str(season))
        log_message("database", "info", "Database disconnected")
        return subdivision
    except Exception as e:
        log_message("database", "error", "There was an error retrieving the postseason start date for season " + str(season) + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return None


def get_team_wins(team):
    """
    Get the team's wins

    :param team:
    :return:
    """

    try:
        log_message("database", "info", "----------------------------")
        log_message("database", "info", "Getting number of wins for " + team)
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT wins FROM teams WHERE (name) IN (('" + team + "'))")
        wins = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info",
                    "Successfully retrieved wins for " + team)
        log_message("database", "info", "Database disconnected")
        return wins

    except Exception as e:
        log_message("database", "error", "There was an issue retrieving wins for " + team + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return False


def get_team_losses(team):
    """
    Get the team's losses

    :param team:
    :return:
    """

    try:
        log_message("database", "info", "----------------------------")
        log_message("database", "info", "Getting number of losses for " + team)
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT losses FROM teams WHERE (name) IN (('" + team + "'))")
        losses = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info",
                    "Successfully retrieved losses for " + team)
        log_message("database", "info", "Database disconnected")
        return losses

    except Exception as e:
        log_message("database", "error", "There was an issue retrieving losses for " + team + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return False


def get_team_win_percentage(team):
    """
    Get the team's win percentage

    :param team:
    :return:
    """

    try:
        log_message("database", "info", "----------------------------")
        log_message("database", "info", "Getting win percentage for " + team)
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT win_percentage FROM teams WHERE (name) IN (('" + team + "'))")
        win_percentage = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info",
                    "Successfully retrieved win percentage for " + team)
        log_message("database", "info", "Database disconnected")
        return win_percentage

    except Exception as e:
        log_message("database", "error", "There was an issue retrieving win percentage for " + team + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return False


def get_season_wins(season, team):
    """
    Get the team's wins for a season

    :param season:
    :param team:
    :return:
    """

    try:
        log_message("database", "info", "----------------------------")
        log_message("database", "info", "Getting number of wins for " + team + " in season " + str(season))
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT wins FROM season_stats WHERE (name, season) IN (('" + team + "', " + str(season) + ")")
        wins = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info",
                    "Successfully retrieved wins for " + team + " in season " + str(season))
        log_message("database", "info", "Database disconnected")
        return wins

    except Exception as e:
        log_message("database", "error", "There was an issue retrieving wins for " + team + " in season " + str(season) + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return False


def get_season_losses(season, team):
    """
    Get the team's losses for a season

    :param season:
    :param team:
    :return:
    """

    try:
        log_message("database", "info", "----------------------------")
        log_message("database", "info", "Getting number of losses for " + team + " in season " + str(season))
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT losses FROM season_stats WHERE (name, season) IN (('" + team + "', " + str(season) + ")")
        losses = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info",
                    "Successfully retrieved losses for " + team + " in season " + str(season))
        log_message("database", "info", "Database disconnected")
        return losses

    except Exception as e:
        log_message("database", "error", "There was an issue retrieving losses for " + team + " in season " + str(season) + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return False


def get_season_win_percentage(season, team):
    """
    Get the team's win percentage for a season

    :param season:
    :param team:
    :return:
    """

    try:
        log_message("database", "info", "----------------------------")
        log_message("database", "info", "Getting win percentage for " + team + " in season " + str(season))
        from fcfb.database.database_administration import connect_to_database
        database = connect_to_database()
        if database is None:
            return None

        cursor = database.cursor()
        cursor.execute("SELECT win_percentage FROM season_stats WHERE (name, season) IN (('" + team + "', " + str(season) + ")")
        win_percentage = cursor.fetchone()[0]

        database.commit()
        cursor.close()
        database.close()
        log_message("database", "info",
                    "Successfully retrieved win percentage for " + team + " in season " + str(season))
        log_message("database", "info", "Database disconnected")
        return win_percentage

    except Exception as e:
        log_message("database", "error", "There was an issue retrieving  win percentage for " + team + " in season " + str(season) + ". " + repr(e))
        log_message("database", "info", "Database disconnected")
        return False