'''
This module includes the class ApiExchange that manages the requests to the crypto exchange done through its API.
Up to now only Cobinhood is supported.
Exchange "simulator" is used for testing.
Created: rggentil
Date: 04/12/18
'''


import logging
import pair
import requests


COBINHOOD = "cobinhood"
SIMULATOR = "simulator"
API_URLS = {COBINHOOD: "https://api.cobinhood.com/v1",
            SIMULATOR: "http://localhost:9071"}


logger = logging.getLogger('rodbot')


class ApiExchangeError(Exception):
    '''
    Error class to report errors in Asset
    '''


class ApiExchange(object):
    '''
    Class to model the api interface of the exchange to operate with
    '''

    def __init__(self, exchange):
        '''
        Constructor
        '''
        self.exchange = exchange
        self.last_pair_stats = self.get_pairs_stats()
        self.btc_usd = pair.Pair(pair_name='BTC-USDT', exchange=exchange)
        self.eth_usd = pair.Pair(pair_name='ETH-USDT', exchange=exchange)
        self.eth_btc = pair.Pair(pair_name='ETH-BTC', exchange=exchange)
        self.update_basic_pairs()

    def update_basic_pairs(self):
        '''
        Update values of paris BTC-USD, ETH-USD, ETH-BTC. Instead of performing 3 requests take the values of the last
        pair stats.
        '''
        logger.debug('Updating basic pairs from exchange %s', self.exchange)
        self.btc_usd.update_values(self.last_pair_stats)
        self.eth_usd.update_values(self.last_pair_stats)
        self.eth_btc.update_values(self.last_pair_stats)

    def get_all_pairs(self):
        '''
        Get all tradeables pairs of the exchange
        :return list_pairs: list of string with string of the pairs
        '''
        api_url = API_URLS[self.exchange]
        logger.debug('Requesting all trading pairs')
        if self.exchange == COBINHOOD or self.exchange == SIMULATOR:
            url = '{}/market/trading_pairs'.format(api_url)
            try:
                r = requests.get(url)
            except requests.ConnectionError:
                logger.error('Error requesting url: %s', url, exc_info=True)
                raise ApiExchangeError
            except Exception:
                logger.error('UNKNOWN ERROR requesting url: %s', url, exc_info=True)
            list_pairs = [pair['id'] for pair in r.json()['result']['trading_pairs']]
        else:
            list_pairs = []
        logger.debug('Available pairs in exchange "%s": %s', self.exchange, list_pairs)
        return list_pairs

    def get_pairs_stats(self, pair='all'):
        '''
        Get stats of the pairs. This stats should include: volume, high24h, low24h, last price, highest bid,
        lowest ask and percentage change 24h.
        :param pair: str. Pair of the stats. Optional, if not provided all stats are returned
        :return: pair_stats: dict with the stats of the pair or of all the pairs
        '''
        logger.debug('Requesting trading stats')
        api_url = API_URLS[self.exchange]
        if self.exchange == COBINHOOD or self.exchange == SIMULATOR:
            url = '{}/market/stats'.format(api_url)
            try:
                r = requests.get(url)
            except requests.ConnectionError:
                logger.error('Error requesting url: %s', url, exc_info=True)
                raise ApiExchangeError
            except Exception:
                logger.error('UNKNOWN ERROR requesting url: %s', url, exc_info=True)
            if pair == 'all':
                pair_stats = r.json()['result']
            else:
                pair_stats = r.json()['result'][pair]
        else:
            pair_stats = {}
        logger.debug('Pair stats in exchange "%s": %s', self.exchange, pair_stats)
        return pair_stats

    def update_stats(self):
        '''
        Method to update stats of the pairs of the exchange
        '''
        self.last_pair_stats = self.get_pairs_stats()

    def get_pairs_by_volume(self, currency=''):
        '''
        Method for obtaining the list of pairs by volume of the exchange. When get the volume by a particular currency,
        the volume obtainted is calculated from the last trade, so this must be not too accurate, other approach could
        be to take the mid range price between asks and bids
        :param currency: str with the short code of the currency we want the volume. If not provided, take default,
                         which is the pair itself.
        :return: dict pair-volume
        '''
        logger.debug('Getting pairs by volume')
        if not currency:
            pairs_volume = {k: float(v['base_volume']) for k, v in self.last_pair_stats.iteritems()}
        else:
            currency_multipliers = get_currency_multiplier(self.last_pair_stats, currency)
            pairs_volume = {k: float(v['base_volume']) * float(v["last_price"]) * currency_multipliers[k]
                            for k, v in self.last_pair_stats.iteritems()}
        logger.debug('Pairs by volume "%s" in exchange "%s": %s', currency, self.exchange, pairs_volume)
        return pairs_volume

    def get_pairs_volume_sorted(self, currency='USD', reverse=True):
        '''
        This method return the list of pairs sorted by volume
        :param currency: str, currency of the volume. Note that the order doesn't change regarding to currency.
                         In USD by default, other options can be BTC or ETH.
        :param reverse: boolean, for the reverse order of the list in ascending or descendin order. Descending (reverse)
                        by default
        :return: list of tuples (pair, volume) in order
        '''
        logger.debug('Getting list of pairs volume "%s" in exchange "%s" sorted: ', currency, self.exchange)
        list_pairs_volume = [(k, v) for k, v in self.get_pairs_by_volume(currency=currency).iteritems()]
        logger.debug('List of pairs volume sorted: %s', list_pairs_volume)
        return sorted(list_pairs_volume, key=lambda x: x[1], reverse=reverse)

    def is_pair_in_exchange(self, pair_id):
        '''
        Check if a particular pair is in the exchange
        :param: pair_id: str of the pair in the form 'XXX-YYY'
        :return: boolean
        '''
        if not pair.check_pair_is_valid(pair_id):
            return False
        else:
            return pair_id in self.get_all_pairs()

    def get_pairs_without_volume(self):
        '''
        Get a list of pairs whose volume is 0
        :return: list of pairs
        '''
        return [k for k, v in self.get_pairs_by_volume().iteritems() if v == 0]


def get_currency_multiplier(pairs_stats, to_currency):
    '''
    Function to know how to multiply pair volume in order to get the volume in a desired currency
    :param pairs_stats: dict with the stats of the pairs
    :param to_currency: str. Currency in which we want the output
    :return: dict with each pair and the float multiplier factor
    '''
    logger.debug('Getting currency multiplier to calculate volume')
    to_currency = 'USDT' if to_currency == 'USD' else to_currency
    pairs_multiplier_factor = dict()
    for pair in pairs_stats.keys():
        base_currency_pair = pair.split('-')[1]
        if base_currency_pair == to_currency:
            pairs_multiplier_factor[pair] = 1
        elif base_currency_pair == 'ETH':
            if to_currency == 'BTC':
                pairs_multiplier_factor[pair] = float(pairs_stats['ETH-BTC']['last_price'])
            elif to_currency == 'USDT':
                pairs_multiplier_factor[pair] = float(pairs_stats['ETH-USDT']['last_price'])
            else:
                logger.error("Exchange to currency %s not available", to_currency)
                raise AttributeError("Exchange to currency %s not available" % to_currency)
        elif base_currency_pair == 'BTC':
            if to_currency == 'ETH':
                pairs_multiplier_factor[pair] = 1 / float(pairs_stats['ETH-BTC']['last_price'])
            elif to_currency == 'USDT':
                pairs_multiplier_factor[pair] = float(pairs_stats['BTC-USDT']['last_price'])
            else:
                logger.error("Exchange to currency %s not available", to_currency)
                raise AttributeError("Exchange to currency %s not available" % to_currency)
        elif 'USD' in base_currency_pair:
            if to_currency == 'ETH':
                pairs_multiplier_factor[pair] = 1 / float(pairs_stats['ETH-USDT']['last_price'])
            elif to_currency == 'BTC':
                pairs_multiplier_factor[pair] = 1 / float(pairs_stats['BTC-USDT']['last_price'])
            else:
                logger.error("Exchange to currency %s not available", to_currency)
                raise AttributeError("Exchange to currency %s not available" % to_currency)
        else:
            pair_trade = '{}-{}'.format(base_currency_pair, to_currency)
            pairs_multiplier_factor[pair] = float(pairs_stats[pair_trade]['last_price'])
    logger.debug('Currency multipliers: %s', pairs_multiplier_factor)
    return pairs_multiplier_factor


if __name__ == "__main__":
    print ApiExchange(COBINHOOD).get_pairs_volume_sorted()
