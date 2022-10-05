import os

from PIL import Image, ImageDraw, ImageFont
import sys

from fcfb.database.retrieve_from_database import *
from fcfb.scorebug.scorebug_utils import *


def convert_to_rgb(hex):
    """
    Convert hex to RGBA
    
    """

    rgb = tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))
    rgb_str = ''
    for value in rgb:
        rgb_str = str(value) + ", " + rgb_str
    return rgb_str


def recolor_team_area(img, home_color, away_color):
    """
    Recolor the team area to the team colors
    
    """

    home_hex = home_color.split("#")[1]
    away_hex = away_color.split("#")[1]

    home_rgb = convert_to_rgb(home_hex)
    away_rgb = convert_to_rgb(away_hex)

    img = img.convert('RGBA')
    pix_data = img.load()

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            # If it is the default yellow
            if pix_data[x, y] == (231, 255, 27, 255):
                r = int(away_rgb.split(", ")[2])
                g = int(away_rgb.split(", ")[1])
                b = int(away_rgb.split(", ")[0])
                pix_data[x, y] = (r, g, b, 255)
            # If it is the default pink
            if pix_data[x, y] == (251, 0, 120, 255):
                r = int(home_rgb.split(", ")[2])
                g = int(home_rgb.split(", ")[1])
                b = int(home_rgb.split(", ")[0])
                pix_data[x, y] = (r, g, b, 255)

    return img


def add_team_names(img, home_team, away_team):
    """
    Add team names to the score bug
    
    """

    home_team_len = len(home_team)
    away_team_len = len(away_team)

    draw = ImageDraw.Draw(img)

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    font_path = main_dir + "/fonts/GazRg-BoldItalic.ttf"

    if home_team_len >= 12:
        home_font = ImageFont.truetype(font_path, 30)
    elif home_team_len > 10:
        home_font = ImageFont.truetype(font_path, 34)
    else:
        home_font = ImageFont.truetype(font_path, 40)
    draw.text((753, 70), home_team, (255, 255, 255), anchor="ra", font=home_font)

    if away_team_len >= 12:
        away_font = ImageFont.truetype(font_path, 30)
    elif away_team_len > 10:
        away_font = ImageFont.truetype(font_path, 34)
    else:
        away_font = ImageFont.truetype(font_path, 40)
    draw.text((63, 70), away_team, (255, 255, 255), anchor="la", font=away_font)

    return img


def add_score(img, home_score, away_score):
    """
    Add score to the score bug
    """

    draw = ImageDraw.Draw(img)

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    font_path = main_dir + "/fonts/GazRg-BoldItalic.ttf"
    font = ImageFont.truetype(font_path, 100)

    draw.text((421, 50), str(home_score), (255, 255, 255), anchor="la", font=font)
    draw.text((380, 50), str(away_score), (255, 255, 255), anchor="ra", font=font)

    return img


def add_possession(img, home_team, away_team, possession, home_score, away_score):
    """
    Add possession to the score bug
    
    """

    draw = ImageDraw.Draw(img)
    if possession == home_team:
        if home_score < 10:
            draw.ellipse((496, 105, 506, 115), fill=(255, 255, 255, 255))
        elif 20 <= home_score < 30:
            draw.ellipse((539, 105, 549, 115), fill=(255, 255, 255, 255))
        elif home_score >= 30:
            draw.ellipse((535, 105, 545, 115), fill=(255, 255, 255, 255))
        else:
            draw.ellipse((520, 105, 530, 115), fill=(255, 255, 255, 255))
    elif possession == away_team:
        if away_score < 10:
            draw.ellipse((310, 105, 320, 115), fill=(255, 255, 255, 255))
        elif away_score < 20:
            draw.ellipse((277, 105, 287, 115), fill=(255, 255, 255, 255))
        else:
            draw.ellipse((260, 105, 270, 115), fill=(255, 255, 255, 255))

    return img


def add_quarter(img, quarter):
    """
    Add quarter to the score bug
    
    """

    draw = ImageDraw.Draw(img)

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    font_path = main_dir + "/fonts/GazRg-BoldItalic.ttf"
    font = ImageFont.truetype(font_path, 40)

    draw.text((67, 161), quarter, (255, 255, 255), font=font)

    return img


def add_clock(img, clock):
    """
    Add clock to the score bug
    
    """

    draw = ImageDraw.Draw(img)

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    font_path = main_dir + "/fonts/GazRg-BoldItalic.ttf"
    font = ImageFont.truetype(font_path, 40)

    draw.text((200, 161), clock, (255, 255, 255), font=font)

    return img


def add_down_and_distance(img, down_and_distance):
    """
    Add down and distance to the score bug
    
    """

    draw = ImageDraw.Draw(img)

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    font_path = main_dir + "/fonts/GazRg-BoldItalic.ttf"
    font = ImageFont.truetype(font_path, 40)

    draw.text((560, 161), down_and_distance, (255, 255, 255), font=font)

    return img


def add_waiting_on(img, waiting_on):
    """
    Add team waiting on to the score bug
    
    """

    waiting_on = waiting_on.upper()
    waiting_on_len = len(waiting_on)

    draw = ImageDraw.Draw(img)

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    font_path = main_dir + "/fonts/GazRg-BoldItalic.ttf"
    font = ImageFont.truetype(font_path, 20)

    if waiting_on_len > 10:
        shift = (waiting_on_len - 7) * 4
    elif waiting_on_len < 5:
        shift = (waiting_on_len - 7) * 1
    else:
        shift = (waiting_on_len - 7) * 3

    draw.text((350, 165), "WAITING ON", (255, 217, 0), font=font)
    draw.text((359 - shift, 185), waiting_on, (255, 217, 0), font=font)

    return img


def add_odds(img, vegas_odds, team, home_team, away_team, shortened_home_team, shortened_away_team):
    """
    Add odds to the score bug
    
    """

    if vegas_odds != "":
        vegas_odds = "(" + str(vegas_odds) + ")"

    home_team_len = len(shortened_home_team)
    away_team_len = len(shortened_away_team)

    draw = ImageDraw.Draw(img)

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    font_path = main_dir + "/fonts/GazRg-BoldItalic.ttf"
    font = ImageFont.truetype(font_path, 25)

    if team == home_team:
        if home_team_len > 10:
            home_shift = (home_team_len - 7) * 4
        elif home_team_len < 5:
            home_shift = (home_team_len - 7) * 15
        else:
            home_shift = (home_team_len - 7) * 15
        draw.text((635 - home_shift, 112), vegas_odds, (255, 255, 255), font=font)
    elif team == away_team:
        if away_team_len > 10:
            away_shift = (away_team_len - 10) * 6
        elif away_team_len < 5:
            away_shift = (away_team_len - 10) * -6
        else:
            away_shift = (away_team_len - 10) * -4
        draw.text((115 - away_shift, 112), vegas_odds, (255, 255, 255), font=font)

    return img


def add_records(img, home_record, away_record):
    """
    Add records to the score bug
    
    """

    draw = ImageDraw.Draw(img)

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    font_path = main_dir + "/fonts/GazRg-BoldItalic.ttf"
    font = ImageFont.truetype(font_path, 30)
    home_wins = int(home_record.split("-")[0].split("(")[1])
    home_losses = int(home_record.split("-")[1].split(")")[0])

    draw.text((749, 118), home_record, (255, 255, 255), anchor="ra", font=font)
    draw.text((55, 118), away_record, (255, 255, 255), anchor="la", font=font)

    return img


def add_final(img):
    """
    Add FINAL indicator to the score bug
    
    """

    draw = ImageDraw.Draw(img)

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    font_path = main_dir + "/fonts/GazRg-BoldItalic.ttf"
    font = ImageFont.truetype(font_path, 40)

    draw.text((350, 161), "FINAL", (255, 217, 0), font=font)

    return img


def draw_ongoing_scorebug(game_id, quarter, clock, cur_down_and_distance, cur_possession, home_team,
                          away_team, home_score, away_score, waiting_on, home_record, away_record):
    """
    Draw the score bug if the game is ongoing

    :param game_id:
    :param quarter:
    :param clock:
    :param cur_down_and_distance:
    :param cur_possession:
    :param home_team:
    :param away_team:
    :param home_score:
    :param away_score:
    :param waiting_on:
    :param home_record:
    :param away_record:
    :return:
    """

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    scorebug_template = main_dir + "/images/scorebug/scorebug_template.png"

    img = Image.open(scorebug_template)

    # Get team colors for plots
    color_dict = get_scorebug_colors(home_team, away_team)
    home_color = color_dict[1]
    away_color = color_dict[2]
    img = recolor_team_area(img, home_color, away_color)

    shortened_home_team = shorten_team_name(home_team)
    shortened_away_team = shorten_team_name(away_team)
    img = add_team_names(img, shortened_home_team, shortened_away_team)

    home_score = int(home_score)
    away_score = int(away_score)
    img = add_score(img, home_score, away_score)

    img = add_possession(img, home_team, away_team, cur_possession, home_score, away_score)

    if quarter == "1":
        quarter = "1st"
    elif quarter == "2":
        quarter = "2nd"
    elif quarter == "3":
        quarter = "3rd"
    elif quarter == "4":
        quarter = "4th"
    img = add_quarter(img, quarter)

    img = add_clock(img, clock)

    img = add_down_and_distance(img, cur_down_and_distance)

    img = add_waiting_on(img, waiting_on)

    if home_record is not None and away_record is not None:
        img = add_records(img, home_record, away_record)

    scorebug_img = main_dir + "/images/scorebug/" + str(game_id) + ".png"
    img.save(scorebug_img)


def draw_final_scorebug(game_id, home_team, away_team, home_score, away_score, home_record, away_record):
    """
    Draw the score bug if the game is final
    
    """

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    scorebug_template = main_dir + "/images/scorebug/scorebug_template.png"
    img = Image.open(scorebug_template)

    color_dict = get_scorebug_colors(home_team, away_team)
    home_color = color_dict[1]
    away_color = color_dict[2]
    img = recolor_team_area(img, home_color, away_color)

    shortened_home_team = shorten_team_name(home_team)
    shortened_away_team = shorten_team_name(away_team)
    img = add_team_names(img, shortened_home_team, shortened_away_team)

    home_score = int(home_score)
    away_score = int(away_score)
    img = add_score(img, home_score, away_score)

    img = add_final(img)

    if home_record is not None and away_record is not None:
        img = add_records(img, home_record, away_record)

    scorebug_img = main_dir + "/images/scorebug/" + str(game_id) + ".png"
    img.save(scorebug_img)
