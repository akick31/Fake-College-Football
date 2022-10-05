import datetime
import json
import discord
import os
from discord.ext import tasks

from fcfb.main.maintain_game_information import *
from fcfb.main.maintain_scoreboard import *
from fcfb.reddit.reddit_games import *


def cyclone_bot(r):
    """
    Run Cyclone Bot infinitely

    """
    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    with open(main_dir + '/configuration/discord_config.json', 'r') as config_file:
        config_data = json.load(config_file)

    token = config_data['discord_token']

    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_message(message):
        message_content = message.content
        # TODO when the command is called to look at a game, grab the game

    @tasks.loop()
    async def maintain_fcfb_data():
        await add_games_from_wiki(r, client, "FakeCollegeFootball")
        await maintain_game_information(r)
        await maintain_scoreboard(r, client)

    @client.event
    async def on_ready():
        print('------')
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

        maintain_fcfb_data.start()
        print('------')
        print('Started maintaining FCFB data')
        print('------')

    client.run(token)

