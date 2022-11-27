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

from fcfb.database.retrieve_from_database import *
from fcfb.database.update_database import *


async def maintain_game_information(r):
    """
    Maintain the game information for all running games

    :param r:
    :return:
    """

    game_links = get_ongoing_game_links()
    for link in game_links:
        link = link[0]
        game_id = get_ongoing_game_id(link)

        if game_id is not None:
            link_id = link.split("/comments")[1]
            submission = r.submission(link_id)

            subdivision = get_ongoing_game_subdivision(game_id)

            from fcfb.reddit_functions.reddit_games import iterate_through_plays
            iterate_through_plays(game_id, submission, subdivision)

            # Done iterating through plays, update the win probability for the scorebug
            win_probability = get_game_plays_win_probability(game_id)
            update_win_probability(game_id, win_probability)
