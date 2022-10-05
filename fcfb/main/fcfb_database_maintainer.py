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

from reddit.reddit_administration import *
from discord_functions.discord_administration import *

if __name__ == '__main__':
    r = login_reddit()

    while True:
        await add_games_from_wiki(r, "FakeCollegeFootball")
        await maintain_game_information(r)
