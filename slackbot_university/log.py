import logging

config = dict(
    log_formatter=(
 	    '%(asctime)s - '
        '%(name)s - '
        '%(funcName)s - '
        '%(levelname)s - '
        '%(message)s'       
    ),
    level=logging.DEBUG
)
logging.basicConfig(
    level=logging.INFO,
    format=config["log_formatter"]
)

def get_logger(name):
    return logging
