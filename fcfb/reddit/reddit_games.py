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

from datetime import datetime
import requests

from database.check_database import *
from database.insert_into_database import *
from database.remove_from_database import *
from database.update_database import *
from discord_functions.discord_utils import *
from reddit.parse_game_thread_info import *
from scorebug.scorebug_drawer import *
from stats.win_probability import *


async def add_games_from_wiki(r, client, subreddit_name):
    """
    Add the ongoing games from the wiki that haven't been added yet, RefBot populates this page

    :param r:
    :param client:
    :param subreddit_name:
    :return:
    """

    games_wiki = r.subreddit(subreddit_name).wiki['games']
    fbs_games = None
    fcs_games = None

    if "FCS" not in games_wiki.content_md and "FBS" not in games_wiki.content_md:
        return
    elif "FCS" in games_wiki.content_md and "FBS" in games_wiki.content_md:
        fbs_games = games_wiki.content_md.split("FCS")[0].split(":-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:")[1].split("\n")
        fcs_games = games_wiki.content_md.split("FCS")[1].split(":-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:")[1].split("\n")
    elif "FCS" not in games_wiki.content_md and "FBS" in games_wiki.content_md:
        fbs_games = games_wiki.content_md.split("FBS")[1].split(":-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:")[1].split("\n")

    season = get_current_season()

    if fbs_games is not None:
        for game in fbs_games:
            if "link" in game:
                game_link = game.split(")|[rerun]")[0].split("[link](")[1]
                game_link_id = game_link.split("/comments")[1]

                submission = r.submission(game_link_id)
                submission_body = submission.selftext

                game_thread_timestamp = datetime.fromtimestamp(submission.created)

                game_id = parse_game_id(submission_body)

                # If the game doesn't exist, parse the info add it to the database
                if game_id is not None and not check_if_game_exists(game_id):
                    game_info = get_game_info(game_id, submission, "FBS")

                    is_final = 1
                    if "Game complete" not in submission_body:
                        is_final = 0
                        insert_into_ongoing_games(game_id, game_link, game_info)
                        draw_ongoing_scorebug(game_id, game_info['quarter'], game_info['clock'],
                                              game_info['down_and_distance'],
                                              game_info['possession'],
                                              game_info['home_team'], game_info['away_team'], game_info['home_score'],
                                              game_info['away_score'],
                                              game_info['team_with_possession'], game_info['home_record'],
                                              game_info['away_record'])
                    else:
                        comment_id = get_discord_comment_id(game_id)
                        if comment_id is not None:
                            scoreboard_channel = get_channel(client, "fcs-scoreboard")
                            comment = await scoreboard_channel.fetch_message(comment_id)
                            comment.delete()

                    insert_into_games(game_id, game_link, game_info, season, is_final, game_thread_timestamp)
    if fcs_games is not None:
        for game in fcs_games:
            if "link" in game:
                game_link = game.split(")|[rerun]")[0].split("[link](")[1]
                game_link_id = game_link.split("/comments")[1]

                submission = r.submission(game_link_id)
                submission_body = submission.selftext

                game_thread_timestamp = datetime.fromtimestamp(submission.created)

                game_id = parse_game_id(submission_body)

                # If the game doesn't exist, parse the info add it to the database
                if game_id is not None and not check_if_game_exists(game_id):
                    game_info = get_game_info(game_id, submission, "FCS")

                    is_final = 1
                    if "Game complete" not in submission_body:
                        is_final = 0
                        insert_into_ongoing_games(game_id, game_link, game_info)
                        draw_ongoing_scorebug(game_id, game_info['quarter'], game_info['clock'],
                                              game_info['down_and_distance'],
                                              game_info['possession'],
                                              game_info['home_team'], game_info['away_team'], game_info['home_score'],
                                              game_info['away_score'],
                                              game_info['team_with_possession'], game_info['home_record'],
                                              game_info['away_record'])
                    else:
                        comment_id = get_discord_comment_id(game_id)
                        if comment_id is not None:
                            scoreboard_channel = get_channel(client, "fcs-scoreboard")
                            comment = await scoreboard_channel.fetch_message(comment_id)
                            comment.delete()

                    insert_into_games(game_id, game_link, game_info, season, is_final, game_thread_timestamp)


def parse_game_id(submission_body):
    """
    Parse the game id from the game thread. The game id is in the gist link.

    :param submission_body:
    :return:
    """

    if "Unable to generate play list" in submission_body:
        return None
    if "Waiting on" in submission_body:
        game_id = submission_body.split("Waiting on")[0].split("[Plays](")[1].split(")")[0].split("Watchful1/")[1]
        return game_id
    else:
        game_id = submission_body.split("Game complete")[0].split("[Plays](")[1].split(")")[0].split("Watchful1/")[1]
        return game_id


def update_game_via_game_thread(game_id, submission, subdivision):
    """
    Update the game in the database

    :param game_id:
    :param submission:
    :param subdivision:
    :return:
    """

    game_info = get_game_info(game_id, submission, subdivision)

    draw_ongoing_scorebug(game_id, game_info['quarter'], game_info['clock'], game_info['down_and_distance'],
                          game_info['possession'],
                          game_info['home_team'], game_info['away_team'], game_info['home_score'],
                          game_info['away_score'],
                          game_info['team_with_possession'], game_info['home_record'], game_info['away_record'])

    update_ongoing_games(game_id, game_info)


def parse_data_from_github(gist_url):
    """
    Parse the data from the Github Gist into data.txt

    :param gist_url:
    :return:
    """

    # Parse data from the github url
    url = gist_url + "/raw"
    gist = requests.get(url)

    # Remove the very first line from the data
    data = ""
    flag = 0
    for character in gist.text:
        if flag == 0 and character == "0":
            data = data + "0"
            flag = 1
        elif flag == 1:
            data = data + character
    if data.find('--------------------------------------------------------------------------------\n') >= 0:
        data = data.replace('--------------------------------------------------------------------------------\n', '-')
    if data.find('--------------------------------------------------------------------------------') >= 0:
        data = data.replace('--------------------------------------------------------------------------------', '-')

    return data


def iterate_through_plays(game_id, submission, subdivision):
    """
    Iterate through the gist and add each line and the win probability to the database

    :param game_id:
    :param submission:
    :param subdivision:
    :return:
    """

    game_info = get_game_info(game_id, submission, subdivision)
    home_team = game_info['home_team']
    away_team = game_info['away_team']
    gist_url = game_info['gist_url']

    gist_data = parse_data_from_github(gist_url)

    # split game into plays
    plays = gist_data.split("\n")
    if "--" in plays:
        plays.remove("--")
    if "-" in plays:
        plays.remove("-")

    num_plays_added = check_number_of_plays(game_id)

    # If the number of plays is the same as the number of plays in the database, you already added everything to add
    if len(plays) == num_plays_added:
        return

    play_number = 1

    for play in plays:

        if "----" not in play and play != "-":
            play_information = play.split("|")
            home_score = play_information[0]
            away_score = play_information[1]
            game_quarter = play_information[2]
            clock = play_information[3]
            ball_location = play_information[4]
            possession = play_information[5]
            down = play_information[6]
            yards_to_go = play_information[7]
            defensive_number = play_information[8]
            if defensive_number == "":
                defensive_number = "0"

            offensive_number = play_information[9]
            if offensive_number == "":
                offensive_number = "0"

            defensive_submitter = play_information[10]
            offensive_submitter = play_information[11]
            play = play_information[12]
            result = play_information[13]
            actual_result = play_information[14]
            yards = play_information[15]
            if yards == "":
                yards = "0"

            play_time = play_information[16]
            if play_time == "":
                play_time = "0"

            runoff_time = play_information[17]
            if runoff_time == "":
                runoff_time = "0"

            if play_number == 1 and possession == "home":
                had_first_possession = 0
            elif play_number == 1 and possession == "away":
                had_first_possession = 1

            win_probability = str(get_current_win_probability(possession, home_team, away_team, home_score, away_score,
                                                              game_quarter, clock, ball_location, down, yards_to_go,
                                                              actual_result, had_first_possession))

            if play_number > num_plays_added:
                insert_play(game_id, home_team, away_team, play_number, home_score, away_score, game_quarter, clock,
                            ball_location, possession, down, yards_to_go, defensive_number, offensive_number,
                            defensive_submitter,
                            offensive_submitter, play, result, actual_result, yards, play_time, runoff_time,
                            win_probability)

            play_number = play_number + 1
