import os


def get_game_info(game_id, submission, subdivision):
    """
    Parse all of the game info from the game thread

    :param submission:
    :param subdivision:
    :return:
    """

    game_info = {
        'home_team': 'none',
        'away_team': 'none',
        'home_coach': 'none',
        'away_coach': 'none',
        'home_offensive_playbook': 'none',
        'away_offensive_playbook': 'none',
        'home_defensive_playbook': 'none',
        'away_defensive_playbook': 'none',
        'home_score': 'none',
        'away_score': 'none',
        'possession': 'none',
        'quarter': 'none',
        'clock': 'none',
        'ball_location': 'none',
        'down_and_distance': 'none',
        'down': 'none',
        'yards_to_go': 'none',
        'team_with_possession': 'none',
        'tv_channel': 'none',
        'start_time': 'none',
        'location': 'none',
        'subdivision': 'none',
        'scorebug': 'none',
        'home_record': 'none',
        'away_record': 'none',
        'gist_url': 'none'
    }

    submission_body = submission.selftext
    submission_title = submission.title

    home_team = parse_home_team(submission_body)
    away_team = parse_away_team(submission_body)
    home_coach = parse_home_coach(submission_body)
    away_coach = parse_away_coach(submission_body)
    game_info['home_team'] = home_team
    game_info['away_team'] = away_team
    game_info['home_coach'] = home_coach
    game_info['away_coach'] = away_coach
    game_info['home_offensive_playbook'] = parse_home_offensive_playbook(submission_body)
    game_info['away_offensive_playbook'] = parse_away_offensive_playbook(submission_body)
    game_info['home_defensive_playbook'] = parse_home_defensive_playbook(submission_body)
    game_info['away_defensive_playbook'] = parse_away_defensive_playbook(submission_body)
    game_info['home_score'] = parse_home_score(submission_body)
    game_info['away_score'] = parse_away_score(submission_body)
    game_info['possession'] = parse_possession(submission_body)
    game_info['quarter'] = parse_quarter(submission_body).split("Q")[0]
    game_info['clock'] = parse_time(submission_body)
    game_info['ball_location'] = parse_yard_line(submission_body)
    down_and_distance = parse_down(submission_body)
    game_info['down_and_distance'] = down_and_distance
    game_info['down'] = down_and_distance.split("&")[0].strip()
    game_info['yards_to_go'] = down_and_distance.split("&")[1].strip()
    game_info['team_with_possession'] = parse_waiting_on(submission_body, home_coach, away_coach, home_team, away_team)
    game_info['tv_channel'] = parse_tv_channel(submission_body)
    game_info['start_time'] = parse_start_time(submission_body)
    game_info['location'] = parse_location(submission_body)
    game_info['subdivision'] = subdivision
    game_info['scorebug'] = "/images/scorebug/" + str(game_id) + ".png"
    game_info['home_record'] = parse_home_record(submission_title)
    game_info['away_record'] = parse_away_record(submission_title)
    game_info['gist_url'] = parse_gist_url_from_game_thread(submission_body)
    return game_info


def parse_waiting_on(submission_body, home_coach, away_coach, home_team, away_team):
    """
    Parse the team that the game is waiting on

    :param submission_body:
    :param home_coach:
    :param away_coach:
    :param home_team:
    :param away_team:
    :return:
    """

    if "Waiting on a response from" in submission_body:
        user = submission_body.split("Waiting on a response from")[1].split("to this")[0].strip()
        if user == home_coach:
            return home_team
        elif user == away_coach:
            return away_team


def parse_home_coach(submission_body):
    """
    Parse the home coach from the game thread

    :param submission_body:
    :return:
    """

    if "**Game Start Time:**" in submission_body and "**Location:**" in submission_body and "**Watch:**" in submission_body:
        home_coach = submission_body.split("___")[0].split("\n")[13].split("|")[1].strip()
    # else there is no game start time or location or watch present
    else:
        home_coach = submission_body.split("___")[0].split("\n")[7].split("|")[1].strip()
    return home_coach


def parse_away_coach(submission_body):
    """
    Parse the away team coach from the game thread

    :param submission_body:
    :return:
    """

    if "**Game Start Time:**" in submission_body and "**Location:**" in submission_body and "**Watch:**" in submission_body:
        away_coach = submission_body.split("___")[0].split("\n")[12].split("|")[1].strip()
    # else there is no game start time or location or watch present
    else:
        away_coach = submission_body.split("___")[0].split("\n")[6].split("|")[1].strip()
    return away_coach


def parse_quarter(submission_body):
    """
    Parse the quarter from the game thread

    :param submission_body:
    :return:
    """

    if len(submission_body.split("___")) == 7:
        quarter = submission_body.split("___")[4].split("\n")[4].split("|")[1].split(" ")[0]
    else:
        quarter = submission_body.split("___")[4].split("\n")[3].split("|")[1].split(" ")[0]
    if quarter == "1":
        return "1Q"
    elif quarter == "2":
        return "2Q"
    elif quarter == "3":
        return "3Q"
    elif quarter == "4":
        return "4Q"
    else:
        return "OT"


def parse_yard_line(submission_body):
    """
    Parse the yard line from the game thread

    :param submission_body:
    :return:
    """

    if len(submission_body.split("___")) == 7:
        # Get the time
        yard_line_field = submission_body.split("___")[4].split("\n")[4].split("|")[3]
        if yard_line_field.strip() != "50":
            side_of_field = yard_line_field.split("]")[0].split("[")[1]
            yard_line = yard_line_field.split("[")[0]
        else:
            return "50"
    else:
        yard_line_field = submission_body.split("___")[3].split("\n")[4].split("|")[3]
        if yard_line_field.strip() != "50":
            side_of_field = yard_line_field.split("]")[0].split("[")[1]
            yard_line = yard_line_field.split("[")[0]
        else:
            return "50"
    return side_of_field + " " + yard_line


def parse_down(submission_body):
    """
    Parse the down from the game thread

    :param submission_body:
    :return:
    """

    if len(submission_body.split("___")) == 7:
        # Get the time
        down = submission_body.split("___")[4].split("\n")[4].split("|")[2]
    else:
        down = submission_body.split("___")[3].split("\n")[4].split("|")[2]
    return down


def parse_possession(submission_body):
    """
    Parse what team has the ball from the game thread

    :param submission_body:
    :return:
    """

    possession = submission_body.split("___")[4].split("\n")[4].split("|")[4].split("]")[0].split("[")[-1]

    if "&amp;" in possession:
        possession = possession.replace("&amp;", "&")

    return possession


def parse_time(submission_body):
    """
    Parse the time from the game thread

    :param submission_body:
    :return:
    """

    if len(submission_body.split("___")) == 7:
        # Get the time
        time = submission_body.split("___")[4].split("\n")[4].split("|")[0]
    else:
        time = submission_body.split("___")[4].split("\n")[3].split("|")[0]
    return time


def parse_home_score(submission_body):
    """
    Parse the home score from the game thread

    :param submission_body:
    :return:
    """

    # Handle various different thread formats
    if len(submission_body.split("___")) == 7:
        scoreboard = submission_body.split("___")[5].split("\n")
        home_team_score = scoreboard[4].split("**")[1]

    elif len(submission_body.split("___")) == 6:
        scoreboard = submission_body.split("___")[5].split("\n")
        home_team_score = scoreboard[4].split("**")[1]

    elif len(submission_body.split("___")) == 5:
        scoreboard = submission_body.split("___")[4].split("\n")
        home_team_score = scoreboard[4].split("**")[1]

    elif len(submission_body.split("___")) == 4:
        scoreboard = submission_body.split("___")[3].split("\n")
        home_team_score = scoreboard[4].split("**")[1]

    elif len(submission_body.split("___")) == 3:
        scoreboard = submission_body.split("___")[2].split("\n")
        home_team_score = scoreboard[3].split("**")[1]

    elif len(submission_body.split("___")) == 1:
        scoreboard = submission_body.split("Q4")[1].split("\n")
        home_team_score = scoreboard[2].split(" | ")[-1]

    else:
        home_team_score = "0"

    return home_team_score


def parse_away_score(submission_body):
    """
    Parse the away score from the game thread

    :param submission_body:
    :return:
    """

    # Handle various different thread formats
    if len(submission_body.split("___")) == 7:
        scoreboard = submission_body.split("___")[5].split("\n")
        away_team_score = scoreboard[5].split("**")[1]

    elif len(submission_body.split("___")) == 6:
        scoreboard = submission_body.split("___")[5].split("\n")
        away_team_score = scoreboard[5].split("**")[1]

    elif len(submission_body.split("___")) == 5:
        scoreboard = submission_body.split("___")[4].split("\n")
        away_team_score = scoreboard[5].split("**")[1]

    elif len(submission_body.split("___")) == 4:
        scoreboard = submission_body.split("___")[3].split("\n")
        away_team_score = scoreboard[5].split("**")[1]

    elif len(submission_body.split("___")) == 3:
        scoreboard = submission_body.split("___")[2].split("\n")
        away_team_score = scoreboard[4].split("**")[1]

    elif len(submission_body.split("___")) == 1:
        scoreboard = submission_body.split("Q4")[1].split("\n")
        away_team_score = scoreboard[3].split(" | ")[-1]

    else:
        away_team_score = "0"

    return away_team_score


def parse_home_team(submission_body):
    """
    Parse the home team from the game thread

    :param submission_body:
    :return:
    """

    home_team = "blank"
    # Handle various different thread formats
    if len(submission_body.split("___")) == 7:
        scoreboard = submission_body.split("___")[5].split("\n")
        home_team = scoreboard[4].split("]")[0]
        home_team = home_team.replace('[', '')

    elif len(submission_body.split("___")) == 6:
        scoreboard = submission_body.split("___")[5].split("\n")
        home_team = scoreboard[4].split("]")[0]
        home_team = home_team.replace('[', '')

    elif len(submission_body.split("___")) == 5:
        scoreboard = submission_body.split("___")[4].split("\n")
        home_team = scoreboard[4].split("]")[0]
        home_team = home_team.replace('[', '')

    elif len(submission_body.split("___")) == 4:
        scoreboard = submission_body.split("___")[3].split("\n")
        home_team = scoreboard[4].split("]")[0]
        home_team = home_team.replace('[', '')

    elif len(submission_body.split("___")) == 3:
        scoreboard = submission_body.split("___")[2].split("\n")
        home_team = scoreboard[3].split("]")[0]
        home_team = home_team.replace('[', '')

    elif len(submission_body.split("___")) == 1:
        scoreboard = submission_body.split("Q4")[1].split("\n")
        home_team = scoreboard[2].split("]")[0]
        home_team = home_team.replace('[', '')

    if "&amp;" in home_team:
        home_team = home_team.replace("&amp;", "&")

    return home_team


def parse_away_team(submission_body):
    """

    :param submission_body:
    :return:
    """

    away_team = "blank"
    # Handle various different thread formats
    if len(submission_body.split("___")) == 7:
        scoreboard = submission_body.split("___")[5].split("\n")
        away_team = scoreboard[5].split("]")[0]
        away_team = away_team.replace('[', '')

    elif len(submission_body.split("___")) == 6:
        scoreboard = submission_body.split("___")[5].split("\n")
        away_team = scoreboard[5].split("]")[0]
        away_team = away_team.replace('[', '')

    elif len(submission_body.split("___")) == 5:
        scoreboard = submission_body.split("___")[4].split("\n")
        away_team = scoreboard[5].split("]")[0]
        away_team = away_team.replace('[', '')

    elif len(submission_body.split("___")) == 4:
        scoreboard = submission_body.split("___")[3].split("\n")
        away_team = scoreboard[5].split("]")[0]
        away_team = away_team.replace('[', '')

    elif len(submission_body.split("___")) == 3:
        scoreboard = submission_body.split("___")[2].split("\n")
        away_team = scoreboard[4].split("]")[0]
        away_team = away_team.replace('[', '')

    elif len(submission_body.split("___")) == 1:
        scoreboard = submission_body.split("Q4")[1].split("\n")
        away_team = scoreboard[3].split("]")[0]
        away_team = away_team.replace('[', '')

    if "&amp;" in away_team:
        away_team = away_team.replace("&amp;", "&")

    return away_team


def parse_home_offensive_playbook(submission_body):
    """
    Parse the home offensive playbook from the game thread

    :param submission_body:
    :return:
    """

    if "**Game Start Time:**" in submission_body and "**Location:**" in submission_body and "**Watch:**" in submission_body:
        home_offensive_playbook = submission_body.split("___")[0].split("\n")[13].split("|")[2].strip()
    # else there is no game start time or location or watch present
    else:
        home_offensive_playbook = submission_body.split("___")[0].split("\n")[7].split("|")[2].strip()
    return home_offensive_playbook


def parse_away_offensive_playbook(submission_body):
    """
    Parse the away offensive playbook from the game thread

    :param submission_body:
    :return:
    """

    if "**Game Start Time:**" in submission_body and "**Location:**" in submission_body and "**Watch:**" in submission_body:
        away_offensive_playbook = submission_body.split("___")[0].split("\n")[12].split("|")[2].strip()
    # else there is no game start time or location or watch present
    else:
        away_offensive_playbook = submission_body.split("___")[0].split("\n")[6].split("|")[2].strip()
    return away_offensive_playbook


def parse_home_defensive_playbook(submission_body):
    """
    Parse the home defensive playbook from the game thread

    :param submission_body:
    :return:
    """

    if "**Game Start Time:**" in submission_body and "**Location:**" in submission_body and "**Watch:**" in submission_body:
        home_defensive_playbook = submission_body.split("___")[0].split("\n")[13].split("|")[3].strip()
    # else there is no game start time or location or watch present
    else:
        home_defensive_playbook = submission_body.split("___")[0].split("\n")[7].split("|")[3].strip()
    return home_defensive_playbook


def parse_away_defensive_playbook(submission_body):
    """
    Parse the away defensive playbook from the game thread

    :param submission_body:
    :return:
    """

    if "**Game Start Time:**" in submission_body and "**Location:**" in submission_body and "**Watch:**" in submission_body:
        away_defensive_playbook = submission_body.split("___")[0].split("\n")[12].split("|")[3].strip()
    # else there is no game start time or location or watch present
    else:
        away_defensive_playbook = submission_body.split("___")[0].split("\n")[6].split("|")[3].strip()
    return away_defensive_playbook


def parse_tv_channel(submission_body):
    """
    Parse the tv channel from the game thread

    :param submission_body:
    :return:
    """

    if "**Watch:**" in submission_body:
        tv_channel = submission_body.split("**Watch:**")[1].split("\n")[0].split("[")[1].split("]")[0].strip()
    # else there is no game start time or location or watch present
    else:
        tv_channel = None
    return tv_channel


def parse_start_time(submission_body):
    """
    Parse the start time from the game thread

    :param submission_body:
    :return:
    """

    if "Start Time:**" in submission_body:
        start_time = submission_body.split("Start Time:**")[1].split("\n")[0].strip()
    else:
        start_time = None
    return start_time


def parse_location(submission_body):
    """
    Parse the location from the game thread

    :param submission_body:
    :return:
    """

    if "Location:**" in submission_body:
        location = submission_body.split("Location:**")[1].split("\n")[0].strip()
    else:
        location = None
    return location


def parse_home_record(title):
    """
    Get the home record from the title

    :param title:
    :return:
    """

    if "@" in title:
        for item in title.split("@")[1].split(" "):
            if "(" in item and "-" in item:
                return item
    return None


def parse_away_record(title):
    """
    Get the away record from the title

    :param title:
    :return:
    """

    if "@" in title:
        for item in title.split("@")[0].split(" "):
            if "(" in item and "-" in item:
                return item
    return None


def parse_gist_url_from_game_thread(submission_body):
    """
    Parse the Gist url from the game thread

    :param submission_body:
    :return:
    """

    if "github" not in submission_body and "pastebin" not in submission_body:
        return None
    elif "Waiting on a response" in submission_body:
        split_list = submission_body.split("Waiting on")[0].split("[Plays](")
        num_items = len(split_list) - 1
        return split_list[num_items].split(")")[0]
    else:
        split_list = submission_body.split("#Game complete")[0].split("[Plays](")
        num_items = len(split_list) - 1
        return split_list[num_items].split(")")[0]
