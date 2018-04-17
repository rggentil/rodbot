'''
This module includes the class Pair to modelize the concept of Pair for future trading. It's not used now, but probably
we'll need it when we have to follow up pairs in different exchanges, with different orders.
Created: rggentil
Date: 04/12/18
'''


import logging
import re


logger = logging.getLogger(__name__)


class Pair(object):
    '''
    This class represents a pair of an exchange
    '''

    def __init__(self, pair_name, exchange):
        '''
        Constructor
        :param pair_name: str with the pair in form XXX-YYY
        :param exchange: str exchange of the pair
        '''
        if check_pair_is_valid(pair_name):
            self.pair_name = pair_name
        else:
            raise AttributeError
        self.exchange = exchange
        self.volume = None
        self.high_24h = None
        self.low_24h = None
        self.last_price = None
        self.last_price_usd = None  # of the first currency of the pair
        self.highest_bid = None
        self.lowest_ask = None
        self.percent_changed_24h = None
        self.in_order_book = None
        self.my_balance_p1 = None
        self.my_balance_p2 = None

    def update_values(self, values_data=None):
        '''
        Function to update the values of the pair by either requesting the pair or processing a json
        :param values_data: dict with the values. Optional, if not a request is performed
        '''
        logger.debug('Updatig values for pair %s', self.pair_name)
        if values_data:
            try:
                self.volume = float(values_data["base_volume"])
                self.high_24h = float(values_data["high_24hr"])
                self.low_24h = float(values_data["low_24hr"])
                self.last_price = float(values_data["last_price"])
                self.highest_bid = float(values_data["highest_bid"])
                self.lowest_ask = float(values_data["lowest_ask"])
                self.percent_changed_24h = float(values_data["percent_changed_24hr"])
            except KeyError:  # This is the cases that we received a dict with all the pairs
                self.update_values(values_data[self.pair_name])
        else:
            raise AttributeError('This function needs data to update, otherwise it fails, need to work on it')


def check_pair_is_valid(pair):
    '''
    Function to check if the pair has a valid format
    :param pair: pair to check
    :return: bool. True if it's OK, False otherwisw
    '''
    return re.search(r'^\w{3,5}-\w{3,5}$', pair) is not None
