import logging
import sys
import os


def create_logger(name):
    """
    Retrieve a logger of the requested name

    """

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filemode='w')

    # Create a custom logger
    logger = logging.getLogger(name)

    # Create handlers
    main_dir = os.path.dirname(os.path.dirname(os.getcwd()))
    log_dir = main_dir + "/logs/"
    log_name = log_dir + name + '.log'
    file_handler = logging.FileHandler(log_name)
    file_handler.setLevel(logging.INFO)

    # Format file
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)

    logger.addHandler(file_handler)
    return logger


def log_message(log_target, level, log_content):
    """
    Log the requested method

    """
    print(level + "-" + log_target + ": " + log_content)

    # if level == "debug":
    #     logger = create_logger(log_target)
    #     logger.debug(log_content)
    #
    # if level == "info":
    #     logger = create_logger(log_target)
    #     logger.info(log_content)
    #
    # if level == "warning":
    #     logger = create_logger(log_target)
    #     logger.warning(log_content)
    #
    if level == "error":
        logger = create_logger(log_target)
        logger.error(log_content)
