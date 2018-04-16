'''
This module contains the api exchange simulator code, that acts like a simple Exchange simulator with predefined
responses, in order to be used in testing (bdd and manual).
Created by: rggentil
Date: 18/04/16
'''

import logging
from flask import Flask, json, jsonify
import flask
from api_exchange_sim_constants import API_EX_SIM_PAIRS_STATS


API_EX_SIM_PATH = ''
API_EX_SIM_HOST = '127.0.0.1'
API_EX_SIM_PORT = 9071


logger = logging.getLogger("api_ex_sim")

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True
app.url_map.strict_slashes = False

logger.info('********* API EXCHANGE SIM started ...............')


class ApiExSimError(Exception):
    def __init__(self, message, status_code=500, payload=None, error_code=5001):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload
        self.error_code = error_code

    def to_dict(self):
        '''
        Tranform response to dict
        :return:
        '''
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(ApiExSimError)
def handle_missing_param(error):
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return '{"code": %d, "description": "%s"}' % (error.error_code, error.message), response.status_code


@app.before_request
def do_before_request():
    """
    Call it before request.
    @return:
    """
    pass


@app.route("/market/trading_pairs", methods=['GET'])
def get_pairs():
    """
    GET for trading pairs of the exchange
    """
    app.logger.info(flask.request.url)
    return jsonify(json.loads(API_EX_SIM_TRADING_PAIRS)), 200


@app.route("/market/stats", methods=['GET'])
def get_trading_stats():
    """
    GET for trading pairs of the exchange
    """
    app.logger.info(flask.request.url)
    return jsonify(json.loads(API_EX_SIM_PAIRS_STATS)), 200


if __name__ == '__main__':
    app.run(host=API_EX_SIM_HOST, port=API_EX_SIM_PORT)
