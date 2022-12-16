from fcfb.reddit_functions.parse_game_thread_info import parse_start_time, get_game_info


def update_game_stats(game_id, play_information):
    """
    Update the game stats for each play

    :param game_id:
    :param play_information:
    :return:
    """

    game_stats = get_game_info(game_id)
    home_pass_attempts = game_stats[19]
    home_pass_completions = game_stats[20]
    home_pass_completion_percentage = game_stats[21]
    home_pass_yards = game_stats[22]
    away_pass_attempts = game_stats[23]
    away_pass_completions = game_stats[24]
    away_pass_completion_percentage = game_stats[25]
    away_pass_yards = game_stats[26]
    home_rush_attempts = game_stats[27]
    home_rush_3_yards_or_more = game_stats[28]
    home_rush_success_percentage = game_stats[29]
    home_rush_yards = game_stats[30]
    away_rush_attempts = game_stats[31]
    away_rush_3_yards_or_more = game_stats[32]
    away_rush_success_percentage = game_stats[33]
    away_rush_yards = game_stats[34]
    home_total_yards = game_stats[35]
    away_total_yards = game_stats[36]
    home_interceptions_lost = game_stats[37]
    home_fumbles_lost = game_stats[38]
    home_turnovers_lost = game_stats[39]
    home_turnover_touchdowns_lost = game_stats[40]
    away_interceptions_lost = game_stats[41]
    away_fumbles_lost = game_stats[42]
    away_turnovers_lost = game_stats[43]
    away_turnover_touchdowns_lost = game_stats[44]
    home_field_goal_made = game_stats[45]
    home_field_goal_attempts = game_stats[46]
    home_field_goal_percentage = game_stats[47]
    home_longest_field_goal = game_stats[48]
    home_blocked_opponent_field_goals = game_stats[49]
    home_field_goal_touchdown = game_stats[50]
    away_field_goal_made = game_stats[51]
    away_field_goal_attempts = game_stats[52]
    away_field_goal_percentage = game_stats[53]
    away_longest_field_goal = game_stats[54]
    away_blocked_opponent_field_goals = game_stats[55]
    away_field_goal_touchdown = game_stats[56]

    home_pass_touchdowns = game_stats[152]
    home_rush_touchdowns = game_stats[153]
    away_pass_touchdowns = game_stats[154]
    away_rush_touchdowns = game_stats[155]
    home_blocked_opponent_punt_td = game_stats[156]
    away_blocked_opponent_punt_td = game_stats[157]

    home_score = play_information[0]
    home_score = str(abs(int(home_score)))
    away_score = play_information[1]
    away_score = str(abs(int(away_score)))

    ball_location = play_information[4]
    possession = play_information[5]
    yards = play_information[15]
    if yards == "":
        yards = 0

    play = play_information[12]
    result = play_information[13]
    actual_result = play_information[14]

    if play == "PASS" and possession == "home":
        home_pass_attempts = home_pass_attempts + 1
        if result == "GAIN":
            home_pass_completions = home_pass_completions + 1
            home_pass_yards = home_pass_yards + yards
            home_total_yards = home_total_yards + yards
        if result == "TURNOVER":
            home_interceptions_lost = home_interceptions_lost + 1
            home_turnovers_lost = home_turnovers_lost + 1
        if result == "TURNOVER_TOUCHDOWN":
            home_interceptions_lost = home_interceptions_lost + 1
            home_turnovers_lost = home_turnovers_lost + 1
            home_turnover_touchdowns_lost = home_turnover_touchdowns_lost + 1
        if actual_result == "TOUCHDOWN":
            home_pass_touchdowns = home_pass_touchdowns + 1
        home_pass_completion_percentage = home_pass_completions/home_pass_attempts

    if play == "PASS" and possession == "away":
        away_pass_attempts = away_pass_attempts + 1
        if result == "GAIN":
            away_pass_completions = away_pass_completions + 1
            away_pass_yards = away_pass_yards + yards
            away_total_yards = away_total_yards + yards
        if result == "TURNOVER":
            away_interceptions_lost = away_interceptions_lost + 1
            away_turnovers_lost = away_turnovers_lost + 1
        if result == "TURNOVER_TOUCHDOWN":
            away_interceptions_lost = away_interceptions_lost + 1
            away_turnovers_lost = away_turnovers_lost + 1
            away_turnover_touchdowns_lost = away_turnover_touchdowns_lost + 1
        if actual_result == "TOUCHDOWN":
            away_pass_touchdowns = away_pass_touchdowns + 1
        away_pass_completion_percentage = away_pass_completions/away_pass_attempts

    if play == "RUN" and possession == "home":
        home_rush_attempts = home_rush_attempts + 1
        if result == "GAIN":
            home_rush_yards = home_rush_yards + yards
            home_total_yards = home_total_yards + yards
            if yards >= 3:
                home_rush_3_yards_or_more = home_rush_3_yards_or_more + 1
        if result == "TURNOVER":
            home_fumbles_lost = home_fumbles_lost + 1
            home_turnovers_lost = home_turnovers_lost + 1
        if result == "TURNOVER_TOUCHDOWN":
            home_fumbles_lost = home_fumbles_lost + 1
            home_turnovers_lost = home_turnovers_lost + 1
            home_turnover_touchdowns_lost = home_turnover_touchdowns_lost + 1
        if actual_result == "TOUCHDOWN":
            home_rush_touchdowns = home_rush_touchdowns + 1
        home_rush_success_percentage = home_rush_3_yards_or_more/home_rush_attempts

    if play == "RUN" and possession == "away":
        away_rush_attempts = away_rush_attempts + 1
        if result == "GAIN":
            away_rush_yards = away_rush_yards + yards
            away_total_yards = away_total_yards + yards
            if yards >= 3:
                away_rush_3_yards_or_more = away_rush_3_yards_or_more + 1
        if result == "TURNOVER":
            away_fumbles_lost = away_fumbles_lost + 1
            away_turnovers_lost = away_turnovers_lost + 1
        if result == "TURNOVER_TOUCHDOWN":
            away_fumbles_lost = away_fumbles_lost + 1
            away_turnovers_lost = away_turnovers_lost + 1
            away_turnover_touchdowns_lost = away_turnover_touchdowns_lost + 1
        if actual_result == "TOUCHDOWN":
            away_rush_touchdowns = away_rush_touchdowns + 1
        away_rush_success_percentage = away_rush_3_yards_or_more/away_rush_attempts

    if play == "FIELD_GOAL" and possession == "home":
        home_field_goal_attempts = home_field_goal_attempts + 1
        if result == "FIELD_GOAL":
            home_field_goal_made = home_field_goal_made + 1
            field_goal_distance = (100-ball_location)+17
            if field_goal_distance > home_longest_field_goal:
                home_longest_field_goal = field_goal_distance
        if result == "TURNOVER":
            away_blocked_opponent_field_goals = away_blocked_opponent_field_goals + 1
            home_turnovers_lost = home_turnovers_lost
        if result == "TURNOVER_TOUCHDOWN":
            away_field_goal_touchdown = away_field_goal_touchdown + 1
            away_blocked_opponent_field_goals = away_blocked_opponent_field_goals + 1
            home_turnover_touchdowns_lost = home_turnover_touchdowns_lost + 1
            home_turnovers_lost = home_turnovers_lost
        home_field_goal_percentage = home_field_goal_made/home_field_goal_attempts

    if play == "FIELD_GOAL" and possession == "away":
        away_field_goal_attempts = away_field_goal_attempts + 1
        if result == "FIELD_GOAL":
            away_field_goal_made = away_field_goal_made + 1
            field_goal_distance = (100-ball_location)+17
            if field_goal_distance > away_longest_field_goal:
                away_longest_field_goal = field_goal_distance
        if result == "TURNOVER":
            home_blocked_opponent_field_goals = home_blocked_opponent_field_goals + 1
            away_turnovers_lost = away_turnovers_lost
        if result == "TURNOVER_TOUCHDOWN":
            home_field_goal_touchdown = home_field_goal_touchdown + 1
            home_blocked_opponent_field_goals = home_blocked_opponent_field_goals + 1
            away_turnover_touchdowns_lost = away_turnover_touchdowns_lost + 1
            away_turnovers_lost = away_turnovers_lost
        away_field_goal_percentage = away_field_goal_made/away_field_goal_attempts

    game_quarter = play_information[2]
    clock = play_information[3]
    ball_location = play_information[4]
    possession = play_information[5]
    down = play_information[6]
    yards_to_go = play_information[7]
    defensive_number = play_information[8]
    if defensive_number == "":
        defensive_number = "0"

    offensive_number = play_information[9]
    if offensive_number == "":
        offensive_number = "0"

    defensive_submitter = play_information[10]
    offensive_submitter = play_information[11]
    play = play_information[12]
    result = play_information[13]
    actual_result = play_information[14]
    yards = play_information[15]
    if yards == "":
        yards = "0"

    play_time = play_information[16]
    if play_time == "":
        play_time = "0"

    runoff_time = play_information[17]
    if runoff_time == "":
        runoff_time = "0"
