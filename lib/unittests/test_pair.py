'''
This module contains the unit tests for module pair.
In general the requests.get method is mocked to returned a pre-defined json instead of requesting exchange for
performance reasons and not depending on third parties.
Created by: rggentil
Date: 18/04/16
'''


import json
import pair
from api_exchange import COBINHOOD
import unittest2 as unittest
from mock import patch
import ut_constants


class TestPair(unittest.TestCase):
    '''
    Tests for Pair class
    '''

    def test_valid_pairs(self):
        self.assertTrue(pair.check_pair_is_valid('BTC-USDT'))
        self.assertTrue(pair.check_pair_is_valid('BTC-LTC'))
        self.assertTrue(pair.check_pair_is_valid('ETH-COB'))
        self.assertTrue(pair.check_pair_is_valid('LALA-USDT'))
        self.assertTrue(pair.check_pair_is_valid('BURGO-USDT'))
        self.assertFalse(pair.check_pair_is_valid('BTC-US'))
        self.assertFalse(pair.check_pair_is_valid('BT-USDT'))
        self.assertFalse(pair.check_pair_is_valid('BTC/USDT'))
        self.assertFalse(pair.check_pair_is_valid('BTCUSDT'))
        self.assertFalse(pair.check_pair_is_valid('BT-ETH'))
        self.assertFalse(pair.check_pair_is_valid('BURGOS-USDT'))
        self.assertFalse(pair.check_pair_is_valid('BTC-CARAME'))

    def test_create_invalid_pair(self):
        self.assertRaises(AttributeError, pair.Pair, pair_name='BURGOS-USDT', exchange='')

    def test_update_pair_with_dict(self):
        my_pair = pair.Pair(pair_name='BTC-USDT', exchange='')
        my_pair_values = {
            "base_volume": 45.6,
            "high_24hr": 11000,
            "low_24hr": 9223,
            "last_price": 9988,
            "highest_bid": 9980,
            "lowest_ask": 9991,
            "percent_changed_24hr": -0.5,
        }

        my_pair.update_values(values_data=my_pair_values)

        self.assertEqual(my_pair.volume, my_pair_values["base_volume"])
        self.assertEquals(my_pair.high_24h, my_pair_values["high_24hr"])
        self.assertEquals(my_pair.high_24h, my_pair_values["high_24hr"])
        self.assertEquals(my_pair.low_24h, my_pair_values["low_24hr"])
        self.assertEquals(my_pair.last_price, my_pair_values["last_price"])
        self.assertEquals(my_pair.highest_bid, my_pair_values["highest_bid"])
        self.assertEquals(my_pair.lowest_ask, my_pair_values["lowest_ask"])
        self.assertEquals(my_pair.percent_changed_24h, my_pair_values["percent_changed_24hr"])

        my_pair_values_error = {
            "base_volume": 45.6,
            "high_24hr": 11000,
        }

        self.assertRaises(KeyError, my_pair.update_values, values_data=my_pair_values_error)

    @patch('lib.api_exchange.requests.get')
    def test_update_pair_with_request(self, mock_get_json):
        mock_get_json.return_value.json.return_value = json.loads(ut_constants.COBINHOOD_PAIRS_STATS)

        def check_pair_data(trading_pair, pair_data):
            trading_pair.update_values(pair_data)
            self.assertEqual(trading_pair.volume, float(pair_data["base_volume"]))
            self.assertEquals(trading_pair.high_24h, float(pair_data["high_24hr"]))
            self.assertEquals(trading_pair.high_24h, float(pair_data["high_24hr"]))
            self.assertEquals(trading_pair.low_24h, float(pair_data["low_24hr"]))
            self.assertEquals(trading_pair.last_price, float(pair_data["last_price"]))
            self.assertEquals(trading_pair.highest_bid, float(pair_data["highest_bid"]))
            self.assertEquals(trading_pair.lowest_ask, float(pair_data["lowest_ask"]))
            self.assertEquals(trading_pair.percent_changed_24h, float(pair_data["percent_changed_24hr"]))

        pair_id1 = 'BTC-USDT'
        my_pair1 = pair.Pair(pair_name=pair_id1, exchange=COBINHOOD)
        pair_data1 = json.loads(ut_constants.COBINHOOD_PAIRS_STATS)['result'][pair_id1]
        pair_id2 = 'COB-ETH'
        my_pair2 = pair.Pair(pair_name=pair_id2, exchange=COBINHOOD)
        pair_data2 = json.loads(ut_constants.COBINHOOD_PAIRS_STATS)['result'][pair_id2]

        check_pair_data(my_pair1, pair_data1)
        check_pair_data(my_pair2, pair_data2)


if __name__ == "__main__":
    unittest.main()
