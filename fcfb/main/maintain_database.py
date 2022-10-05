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

from main.maintain_game_information import maintain_game_information
from reddit.reddit_games import add_games_from_wiki


async def database_bot(r):
    """
    Run the database maintainer portion of Cyclone Bot

    :param r:
    :return:
    """

    while True:
        await add_games_from_wiki(r, "FakeCollegeFootball")
        await maintain_game_information(r)
