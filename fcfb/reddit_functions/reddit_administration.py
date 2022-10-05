import praw
import json
import os


def login_reddit():
    """
    Login to reddit

    """

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    with open(main_dir + '/configuration/reddit_config.json', 'r') as config_file:
        config_data = json.load(config_file)

    r = praw.Reddit(user_agent=config_data['user_agent'],
                    client_id=config_data['client_id'],
                    client_secret=config_data['client_secret'],
                    username=config_data['username'],
                    password=config_data['password'],
                    subreddit=config_data['subreddit'],
                    check_for_async=False)
    return r
