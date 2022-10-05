"""
1313 Bot handles the scoreboard and various other score queries for FCFB

@author: apkick

"""

import os

from fcfb.database.retrieve_from_database import *
from fcfb.reddit.reddit_games import add_games_from_wiki
from fcfb.reddit.reddit_administration import *
from fcfb.discord.discord_administration import *

if __name__ == '__main__':
    r = login_reddit()
    cyclone_bot(r)
