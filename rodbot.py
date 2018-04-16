'''
Simple script/bot to manage trading in exchanges
Author: Rodrigo Gomez Gentil
Date: 03/27/18
'''

import argparse
from src import api_exchange
import json
import logging
from logging.config import dictConfig
from datetime import datetime
import os
from time import sleep
import sys


VOLUME_PAIRS_FILE = os.path.join('out', 'pairs_volume.json')
TRADING_LOG = os.path.join('log', 'rodbot.{}')


dict_log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s.%(filename)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level":"INFO",
            "class":"logging.StreamHandler",
            # "formatter": "standard"
        },
        "file_debug": {
            "level":"DEBUG",
            "class":"logging.FileHandler",  # Other option might be logging.handlers.RotatingFileHandler
            "formatter": "standard",
            "filename": TRADING_LOG.format('debug')
        },
        "file_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": TRADING_LOG.format('info')
        },
        "file_error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": TRADING_LOG.format('error')
        }
    },
    "loggers": {
        "": {
            "handlers": ["console", "file_debug", "file_info", "file_error"],
            "level": "INFO",
            "propagate": True
        }
    }
}
dictConfig(dict_log_config)
logger = logging.getLogger('rodbot')


def get_parsed_args():
    '''
    Function to manage parsed arguments
    :return: parse args
    '''
    parser = argparse.ArgumentParser(description='Simple script/bot to manage trading in exchanges')

    parser.add_argument('-x', '--exchange', default='cobinhood', choices=['cobinhood', 'simulator'],
                        help='Select exchange to operate with.')
    parser.add_argument('-c', '--currency', default='USD', choices=['USD', 'BTC', 'ETH'],
                        help='Select exchange to operate with.')
    parser.add_argument('-i', '--interval', default=600, type=int, help='checking interval')
    parser.add_argument('-v', '--verbosity', action='count', help='increase output verbosity')

    return parser.parse_args()


def setup_log_level(verbosity):
    '''
    Set up and define log level
    :param verbosity: level of verbosity of logs
    '''
    if verbosity >= 1:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
        # I dont like too much how Im managing this but I dont see other options. The way we remove debug file handler
        # is not the best way but trying to get the handler by name, using a "private" var isn't either a good way.
        # debug_handler = [h for h in logger.root.handlers if h._name == 'file_debug'][0]
        logger.root.removeHandler(logger.root.handlers[1])

    logger.setLevel(log_level)


def main():
    parsed_args = get_parsed_args()

    setup_log_level(parsed_args.verbosity)
    logger.debug('Parsed args: %s', parsed_args)

    logger.debug('Prepare requesting api exchange')

    try:
        e = api_exchange.ApiExchange(exchange=parsed_args.exchange)
    except api_exchange.ApiExchangeError:
        logger.error('Error when trying to start connection with exchange "%s"', parsed_args.exchange)
        sys.exit(1)

    try:
        while True:
            try:
                get_volume(e, parsed_args)
            except api_exchange.ApiExchangeError:
                logger.error('Error getting volume in exchange "%s"', parsed_args.exchange)
            sleep(parsed_args.interval)
    except KeyboardInterrupt:
        print
        logger.info('Stopping rodbot...\n')
        sys.exit(0)


def get_volume(e, parsed_args):
    '''
    Function to log volume of trading pairs
    :param e: ApiExchange object
    :param parsed_args: parser object with arguments
    '''
    e.update_stats()
    pairs_volume = e.get_pairs_by_volume()
    pairs_volume_sorted = e.get_pairs_volume_sorted(currency=parsed_args.currency)
    volume_pairs_dict = {'time': datetime.isoformat(datetime.now()),
                         'pairs_volume': pairs_volume,
                         'pairs_volume_sorted': pairs_volume_sorted,
                         'pairs_withouth_volume': e.get_pairs_without_volume()}
    logger.debug('Storing pairs volume data in %s', VOLUME_PAIRS_FILE)
    with open(VOLUME_PAIRS_FILE, 'w') as f:
        json.dump(volume_pairs_dict, f, indent=4)

    logger.info('-trading- Top 10 pairs by volume %s', pairs_volume_sorted[0:9])


if __name__ == '__main__':
    main()
