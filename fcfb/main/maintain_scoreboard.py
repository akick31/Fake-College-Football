import sys
import os
import time

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from discord_functions.discord_comments import *
from reddit.reddit_games import *
from scorebug.scorebug_drawer import *
from database.update_database import *


async def maintain_scoreboard(r, client):
    """
    Maintain the scoreboards on the Discord server

    :param r:
    :param client:
    :return:
    """

    game_links = get_ongoing_game_links()
    for link in game_links:
        link = link[0]
        game_id = get_ongoing_game_id(link)

        if game_id is not None:
            time.sleep(5)
            discord_comment_id = get_discord_comment_id(game_id)
            subdivision = get_ongoing_game_subdivision(game_id)
            is_done = check_game_done(game_id)

            if discord_comment_id is not None:
                link_id = link.split("/comments")[1]
                submission = r.submission(link_id)

                # If game is done, mark it as done and delete from scoreboard
                if "Game complete" in submission.selftext:
                    await handle_game_over(client, game_id, submission, subdivision)
                else:
                    update_game_via_game_thread(game_id, submission, subdivision)
                    await edit_scoreboard(r, client, game_id, link, subdivision)
            elif is_done == 0 and discord_comment_id is None:
                discord_comment_id = await add_game_to_scoreboard(r, client, game_id, link, subdivision)
                update_discord_comment_id_into_ongoing_games(game_id, discord_comment_id)


async def handle_game_over(client, game_id, submission, subdivision):
    """
    Refbot marked the game as over, handle updating the scorebug and more

    :param client:
    :param game_id:
    :param submission:
    :param subdivision:
    :return:
    """

    comment_id = get_discord_comment_id(game_id)

    if subdivision == "FBS":
        scoreboard_channel = get_channel(client, "fbs-scoreboard")
    elif subdivision == "FCS":
        scoreboard_channel = get_channel(client, "fcs-scoreboard")

    comment = await scoreboard_channel.fetch_message(comment_id)
    await comment.delete()

    remove_game_from_ongoing_games(game_id)
    mark_game_done(game_id)

    game_info = get_game_info(game_id, submission, subdivision)
    draw_final_scorebug(game_id, game_info['home_team'], game_info['away_team'], game_info['home_score'],
                        game_info['away_score'], game_info['home_record'], game_info['away_record'])
