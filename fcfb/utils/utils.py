def calculate_vegas_odds(team_elo, opponent_elo):
    """
    Calculate Vegas odds using a constant and team and their opponent Elo

    :param team_elo:
    :param opponent_elo:
    :return:
    """

    constant = 18.14010981807
    odds = (float(opponent_elo) - float(team_elo))/constant
    return odds


def get_vegas_odds(home_team, away_team):
    """
    Return a dictionary containing the Vegas Odds for the game

    :param home_team:
    :param away_team:
    :param database:
    :return:
    """

    from database.retrieve_from_database import get_elo
    home_elo = get_elo(home_team)
    away_elo = get_elo(away_team)
    if home_elo is None or away_elo is None:
        return None

    home_odds = calculate_vegas_odds(home_elo, away_elo)
    away_odds = calculate_vegas_odds(away_elo, home_elo)

    # Default to a push if can't find Elo
    if home_elo == -500 or away_elo == -500:
        home_odds = 0
        away_odds = 0
    return{'home_odds': home_odds, 'away_idds': away_odds}
