'''
This module contains the unit tests for module api_exchange.
In general the requests.get method is mocked to returned a pre-defined json instead of requesting exchange for
performance reasons and not depending on third parties.
Created by: rggentil
Date: 18/04/16
'''


import json
import unittest
from mock import patch
import requests
import ut_constants
from api_exchange import ApiExchange, COBINHOOD, get_currency_multiplier, ApiExchangeError


class TestApiExchange(unittest.TestCase):
    '''
    Tests for Pair class
    '''

    def setUp(self):
        self.mock_get_json = patch('api_exchange.requests.get')
        # self.addCleanup(self.mock_get_json.stop) We supposed need this in order to avoid mock on if set up fails
        # but if I leave this the tests don't work. NEET TO BE STUDY
        self.mock_get = self.mock_get_json.start()
        self.mock_get.return_value.json.return_value = json.loads(ut_constants.COBINHOOD_PAIRS_STATS)
        self.api_cobinhood = ApiExchange(COBINHOOD)
        self.cobinhood_pairs_stats = json.loads(ut_constants.COBINHOOD_PAIRS_STATS)['result']

    def tearDown(self):
        self.mock_get_json.stop()

    def test_get_pairs_stats(self):
        self.assertEquals(self.api_cobinhood.get_pairs_stats(), self.cobinhood_pairs_stats)
        self.assertEquals(self.api_cobinhood.get_pairs_stats('all'), self.cobinhood_pairs_stats)
        self.assertEquals(self.api_cobinhood.get_pairs_stats('BTC-USDT'), self.cobinhood_pairs_stats['BTC-USDT'])

    def test_get_pairs_by_volume(self):
        # Volume by pair itself
        pairs_volume = {k: float(v['base_volume']) for k, v in self.cobinhood_pairs_stats.iteritems()}
        self.assertEquals(self.api_cobinhood.get_pairs_by_volume(), pairs_volume)

        # Volume for different currencies
        for currency in ['BTC', 'ETH', 'USD', 'USDT']:
            currency_multiplier = get_currency_multiplier(self.cobinhood_pairs_stats, currency)
            pairs_volume = {k: float(v['base_volume']) * float(v["last_price"]) * currency_multiplier[v['id']]
                            for k, v in json.loads(ut_constants.COBINHOOD_PAIRS_STATS)['result'].iteritems()}
            self.assertEquals(self.api_cobinhood.get_pairs_by_volume(currency=currency), pairs_volume)

        self.assertRaises(AttributeError, self.api_cobinhood.get_pairs_by_volume, currency='ENJ')

    def test_update_basic_pairs(self):
        self.assertEquals(self.api_cobinhood.btc_usd.last_price,
                          float(self.cobinhood_pairs_stats['BTC-USDT']["last_price"]))
        self.assertEquals(self.api_cobinhood.eth_usd.last_price,
                          float(self.cobinhood_pairs_stats['ETH-USDT']["last_price"]))
        self.assertEquals(self.api_cobinhood.eth_btc.last_price,
                          float(self.cobinhood_pairs_stats['ETH-BTC']["last_price"]))

    def test_currency_multiplier(self):
        self.assertEquals(get_currency_multiplier(self.cobinhood_pairs_stats, 'BTC')['LTC-BTC'], 1)
        self.assertEquals(get_currency_multiplier(self.cobinhood_pairs_stats, 'BTC')['COB-BTC'], 1)
        self.assertEquals(get_currency_multiplier(self.cobinhood_pairs_stats, 'ETH')['COB-ETH'], 1)
        self.assertEquals(get_currency_multiplier(self.cobinhood_pairs_stats, 'USDT')['ENJ-USDT'], 1)
        self.assertEquals(get_currency_multiplier(self.cobinhood_pairs_stats, 'BTC')['COB-ETH'],
                          self.api_cobinhood.eth_btc.last_price)
        self.assertEquals(get_currency_multiplier(self.cobinhood_pairs_stats, 'ETH')['COB-BTC'],
                          1 / self.api_cobinhood.eth_btc.last_price)
        self.assertEquals(get_currency_multiplier(self.cobinhood_pairs_stats, 'USD')['COB-BTC'],
                          self.api_cobinhood.btc_usd.last_price)
        self.assertEquals(get_currency_multiplier(self.cobinhood_pairs_stats, 'BTC')['CMT-USDT'],
                          1 / self.api_cobinhood.btc_usd.last_price)
        self.assertEquals(get_currency_multiplier(self.cobinhood_pairs_stats, 'ETH')['LTC-BTC'],
                          1 / self.api_cobinhood.eth_btc.last_price)
        self.assertEquals(get_currency_multiplier(self.cobinhood_pairs_stats, 'ETH')['LTC-USDT'],
                          1 / self.api_cobinhood.eth_usd.last_price)
        self.assertEquals(get_currency_multiplier(self.cobinhood_pairs_stats, 'BTC')['CMT-COB'],
                          float(self.cobinhood_pairs_stats['COB-BTC']["last_price"]))
        self.assertRaises(AttributeError, get_currency_multiplier, self.cobinhood_pairs_stats, 'ENJ')

    def test_get_pairs_volume_sorted(self):
        list_pairs_volume = [(k, v) for k, v in
                             self.api_cobinhood.get_pairs_by_volume(currency='USD').iteritems()]
        self.assertEquals(self.api_cobinhood.get_pairs_volume_sorted(currency='USD', reverse=True),
                          sorted(list_pairs_volume, key=lambda x: x[1], reverse=True))
        self.assertEquals(self.api_cobinhood.get_pairs_volume_sorted(),
                          sorted(list_pairs_volume, key=lambda x: x[1], reverse=True))

        list_pairs_volume = [(k, v) for k, v in
                             self.api_cobinhood.get_pairs_by_volume(currency='BTC').iteritems()]
        self.assertEquals(self.api_cobinhood.get_pairs_volume_sorted(currency='BTC'),
                          sorted(list_pairs_volume, key=lambda x: x[1], reverse=True))

        list_pairs_volume = [(k, v) for k, v in
                             self.api_cobinhood.get_pairs_by_volume(currency='ETH').iteritems()]
        self.assertEquals(self.api_cobinhood.get_pairs_volume_sorted(currency='ETH', reverse=False),
                          sorted(list_pairs_volume, key=lambda x: x[1], reverse=False))

    @patch('api_exchange.ApiExchange.get_all_pairs')
    def test_is_pair_in_exchange(self, mock_get_all_pairs):
        mock_get_all_pairs.return_value = ut_constants.COBINHOOD_PAIRS
        self.assertTrue(self.api_cobinhood.is_pair_in_exchange('BTC-USDT'))
        self.assertFalse(self.api_cobinhood.is_pair_in_exchange('PST-EUR'))
        self.assertFalse(self.api_cobinhood.is_pair_in_exchange('MORTADELOS-EUR'))

    @patch('api_exchange.requests.get')
    def test_error_connection(self, mock_connection_error):
        e = ApiExchange(COBINHOOD)

        mock_connection_error.side_effect = requests.ConnectionError
        self.assertRaises(ApiExchangeError, e.get_all_pairs)
        self.assertRaises(ApiExchangeError, e.get_pairs_stats)

        self.assertRaises(ApiExchangeError, ApiExchange, COBINHOOD)

    def test_get_pairs_without_volume(self):
        pairs_no_volume = [k for k, v in self.cobinhood_pairs_stats.iteritems() if float(v['base_volume']) == 0]
        self.assertItemsEqual(self.api_cobinhood.get_pairs_without_volume(), pairs_no_volume)


@unittest.skip("Test only for comparing api data returned structure")
class TestRealAPi(unittest.TestCase):
    '''
    Test to check that the connection with real API is ok and data structure hasn't changed
    '''

    def setUp(self):
        self.api_cobinhood = ApiExchange(COBINHOOD)
        self.cobinhood_pairs_stats = json.loads(ut_constants.COBINHOOD_PAIRS_STATS)['result']

    def test_pair_stats_structure(self):
        self.assertEquals(self.cobinhood_pairs_stats['ETH-BTC'].keys(),
                          self.api_cobinhood.get_pairs_stats('ETH-BTC').keys())


if __name__ == "__main__":
    unittest.main()
