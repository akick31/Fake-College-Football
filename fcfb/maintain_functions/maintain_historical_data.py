from datetime import datetime
from psaw import PushshiftAPI
from reddit_functions.reddit_games import *


def historical_bot(r):
    iterate_through_season(r, 2)
    iterate_through_season(r, 3)
    iterate_through_season(r, 4)
    iterate_through_season(r, 5)
    iterate_through_season(r, 6)


def iterate_through_season(r, season):
    search_item = "\"Game Thread\""

    season_start = get_season_start(season)
    season_end = get_season_end(season)
    postseason_start = get_postseason_start(season)

    api = PushshiftAPI()

    limit = 100000
    game_list = list(api.search_submissions(search_item=search_item, subreddit="FakeCollegeFootball", after=season_start, before=season_end,
                                            filter=['url', 'title', 'created'], limit=limit))

    for submission in game_list:
        game_thread_timestamp = datetime.fromtimestamp(submission.created)

        game_link = submission.url

        if "game_thread" in game_link and "post_game_thread" not in game_link:
            link_id = game_link.split("/comments")[1]
            submission = r.submission(link_id)
            submission_body = submission.selftext

            game_id = parse_game_id(submission_body)

            home_team = parse_home_team(submission_body)
            away_team = parse_away_team(submission_body)

            # If the game doesn't exist, parse the info add it to the database
            if game_id is not None and "scrimmage" not in submission.title.lower() \
                    and "post game thread" not in submission.title.lower() and "megabracket" not in submission.title.lower() \
                    and check_if_team_exists(home_team) and check_if_team_exists(away_team) \
                    and not check_if_game_exists_in_games(game_id):

                print(submission.title)

                subdivision = get_team_subdivision(parse_home_team(submission_body))
                if subdivision is None:
                    subdivision = "D2"

                game_info = get_game_info(game_id, submission, subdivision)

                insert_into_games(game_id, game_link, game_info, season, 1, game_thread_timestamp)

                if int(game_info['home_score']) > int(game_info['away_score']):
                    home_wins = get_team_wins(game_info['home_team'])
                    home_losses = get_team_wins(game_info['home_team'])
                    home_win_percentage = int(home_wins)/int(home_losses)
                    update_team_wins(game_info['home_team'], home_wins)
                    update_team_win_percentage(game_info['home_team'], home_win_percentage)

                    away_wins = get_team_wins(game_info['away_team'])
                    away_losses = get_team_wins(game_info['away_team'])
                    away_win_percentage = int(away_wins) / int(away_losses)
                    update_team_losses(game_info['away_team'], away_losses)
                    update_team_win_percentage(game_info['away_team'], away_win_percentage)

                    home_wins = get_season_wins(season, game_info['home_team'])
                    home_losses = get_season_wins(season, game_info['home_team'])
                    home_win_percentage = int(home_wins) / int(home_losses)
                    update_season_wins(season, game_info['home_team'], home_wins)
                    update_season_win_percentage(season, game_info['home_team'], home_win_percentage)

                    away_wins = get_season_wins(season, game_info['away_team'])
                    away_losses = get_season_wins(season, game_info['away_team'])
                    away_win_percentage = int(away_wins) / int(away_losses)
                    update_season_losses(season, game_info['away_team'], away_losses)
                    update_season_win_percentage(season, game_info['away_team'], away_win_percentage)

                elif int(game_info['away_score']) > int(game_info['home_score']):
                    home_wins = get_team_wins(game_info['home_team'])
                    home_losses = get_team_wins(game_info['home_team'])
                    home_win_percentage = int(home_wins) / int(home_losses)
                    update_team_losses(game_info['home_team'], home_wins)
                    update_team_win_percentage(game_info['home_team'], home_win_percentage)

                    away_wins = get_team_wins(game_info['away_team'])
                    away_losses = get_team_wins(game_info['away_team'])
                    away_win_percentage = int(away_wins) / int(away_losses)
                    update_team_wins(game_info['away_team'], away_losses)
                    update_team_win_percentage(game_info['away_team'], away_win_percentage)

                    home_wins = get_season_wins(season, game_info['home_team'])
                    home_losses = get_season_wins(season, game_info['home_team'])
                    home_win_percentage = int(home_wins) / int(home_losses)
                    update_season_losses(season, game_info['home_team'], home_wins)
                    update_season_win_percentage(season, game_info['home_team'], home_win_percentage)

                    away_wins = get_season_wins(season, game_info['away_team'])
                    away_losses = get_season_wins(season, game_info['away_team'])
                    away_win_percentage = int(away_wins) / int(away_losses)
                    update_season_wins(season, game_info['away_team'], away_losses)
                    update_season_win_percentage(season, game_info['away_team'], away_win_percentage)

