import discord
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

from discord_functions.discord_utils import *
from logs.logs import *
from reddit_functions.parse_game_thread_info import *
from utils.utils import *


async def add_game_to_scoreboard(r, client, game_id, game_link, subdivision):
    """
    Add game to scoreboard channel

    :param r:
    :param client:
    :param game_id:
    :param game_link:
    :param subdivision:
    :return:
    """

    game_link_id = game_link.split("/comments")[1]
    submission = r.submission(game_link_id)
    game_info = get_game_info(game_id, submission, subdivision)

    vegas_odds = get_vegas_odds(game_info['home_team'], game_info['away_team'])

    if vegas_odds is None:
        odds_text = "Push"
    else:
        odds = round(vegas_odds['home_odds'] * 2) / 2
        if odds == 0:
            odds_text = "Push"
        elif odds > 0:
            odds_text = game_info['home_team'] + " +" + str(odds)
        else:
            odds_text = game_info['home_team'] + " " + str(odds)

    from database.retrieve_from_database import get_win_probability
    win_probability = get_win_probability(game_id)

    if win_probability is None or int(win_probability) == 50:
        win_text = "Each team has a 50% chance to win\n"
    elif int(win_probability) >= 50:
        win_text = game_info['home_team'] + " has a " + str(int(win_probability)) + "% chance to win\n"
    elif int(win_probability) < 50:
        win_text = game_info['away_team'] + " has a " + str(100 - int(win_probability)) + "% chance to win\n"

    embed = discord.Embed(title="**Game Information**", color=0x005EB8)
    embed.add_field(name="**Watch**", value="[Game Thread](" + game_link + ")", inline=False)
    embed.add_field(name="**Spread**", value=odds_text, inline=False)
    embed.add_field(name="**Win Probability**", value=win_text, inline=False)

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    from database.retrieve_from_database import get_scorebug
    scorebug = get_scorebug(game_id)

    with open(main_dir + scorebug, 'rb') as fp:
        file = discord.File(fp, 'posted_scorebug.png')
        embed.set_image(url="attachment://posted_scorebug.png")

    embed.add_field(name="**Ball Location**", value=game_info['ball_location'], inline=False)

    if subdivision == "FBS":
        scoreboard_channel = get_channel(client, "fbs-scoreboard")
    elif subdivision == "FCS":
        scoreboard_channel = get_channel(client, "fcs-scoreboard")
    comment = await scoreboard_channel.send(embed=embed, file=file)

    return comment.id


async def edit_scoreboard(r, client, game_id, game_link, subdivision):
    """
    Edit the scoreboard in the scoreboard channel

    :param r:
    :param client:
    :param game_id:
    :param game_link:
    :param subdivision:
    :return:
    """

    game_link_id = game_link.split("/comments")[1]
    submission = r.submission(game_link_id)
    game_info = get_game_info(game_id, submission, subdivision)

    vegas_odds = get_vegas_odds(game_info['home_team'], game_info['away_team'])

    if vegas_odds is None:
        odds_text = "Push"
    else:
        odds = round(vegas_odds['home_odds'] * 2) / 2
        if odds == 0:
            odds_text = "Push"
        elif odds > 0:
            odds_text = game_info['home_team'] + " +" + str(odds)
        else:
            odds_text = game_info['home_team'] + " " + str(odds)

    from database.retrieve_from_database import get_win_probability
    win_probability = get_win_probability(game_id)

    if win_probability is None or int(win_probability) == 50:
        win_text = "Each team has a 50% chance to win\n"
    elif int(win_probability) >= 50:
        win_text = game_info['home_team'] + " has a " + str(int(win_probability)) + "% chance to win\n"
    elif int(win_probability) < 50:
        win_text = game_info['away_team'] + " has a " + str(100 - int(win_probability)) + "% chance to win\n"

    embed = discord.Embed(title="**Game Information**", color=0x005EB8)
    embed.add_field(name="**Watch**", value="[Game Thread](" + game_link + ")", inline=False)
    embed.add_field(name="**Spread**", value=odds_text, inline=False)
    embed.add_field(name="**Win Probability**", value=win_text, inline=False)

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    from database.retrieve_from_database import get_scorebug
    scorebug = get_scorebug(game_id)

    with open(main_dir + scorebug, 'rb') as fp:
        file = discord.File(fp, 'posted_scorebug.png')
        embed.set_image(url="attachment://posted_scorebug.png")

    embed.add_field(name="**Ball Location**", value=game_info['ball_location'], inline=False)

    from database.retrieve_from_database import get_discord_comment_id
    comment_id = get_discord_comment_id(game_id)
    if subdivision == "FBS":
        scoreboard_channel = get_channel(client, "fbs-scoreboard")
    elif subdivision == "FCS":
        scoreboard_channel = get_channel(client, "fcs-scoreboard")

    comment = await scoreboard_channel.fetch_message(comment_id)
    await comment.remove_attachments(comment.attachments)
    await comment.add_files(file)
    await comment.edit(embed=embed)


async def post_comment(message, comment_content):
    """
    Post a generic comment on Discord

    :param message:
    :param comment_content:
    :return:
    """

    try:
        await message.channel.send(comment_content)
        return True
    except Exception as e:
        await log_message("discord", "error", repr(e))
        return False
