import asyncio
import inspect
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

from reddit.reddit_administration import login_reddit
from main.maintain_database import database_bot

if __name__ == '__main__':
    r = login_reddit()

    if inspect.iscoroutinefunction(database_bot):
        task = database_bot(r)
        res = asyncio.get_event_loop().run_until_complete(task)


