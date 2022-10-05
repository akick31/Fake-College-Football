from fcfb.database.retrieve_from_database import *
from fcfb.database.update_database import *
from fcfb.reddit.reddit_games import iterate_through_plays


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

        link_id = link.split("/comments")[1]
        submission = r.submission(link_id)

        subdivision = get_ongoing_game_subdivision(game_id)

        iterate_through_plays(game_id, submission, subdivision)

        # Done iterating through plays, update the win probability for the scorebug
        win_probability = get_game_plays_win_probability(game_id)
        update_win_probability(game_id, win_probability)
