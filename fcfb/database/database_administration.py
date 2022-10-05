import json
import mysql
import mysql.connector
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

from logs.logs import *


def connect_to_database():
    """
    Connect to the FCFB database

    """

    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    with open(main_dir + '/configuration/database_config.json', 'r') as config_file:
        config_data = json.load(config_file)

    database = mysql.connector.connect(
        host=config_data['database_host'],
        user=config_data['database_user'],
        passwd=config_data['database_password'],
        database=config_data['database'],
    )

    if database.is_connected():
        log_message("database", "info", "Connected to the FCFB Database")
    else:
        log_message("database", "error", "Could not connect to the FCFB Database")
        return

    return database

