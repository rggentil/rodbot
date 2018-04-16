'''
This module contains the step for behave tests to check the api exchange
Created by: rggentil
Date: 18/04/16
'''

from behave import *

from datetime import datetime, timedelta
import logging
import requests
import subprocess
from time import sleep
import os
import sys
import json
from bdd.api_exchange_simulator.api_exchange_sim_constants import API_EX_SIM_PAIRS_STATS


VOLUME_PAIRS_FILE = os.path.join('out', 'pairs_volume.json')


logger = logging.getLogger('behave')


use_step_matcher("re")


@given('.* tradeable pairs?')
def step_existing_pairs(context):
    """
    Just semantic step
    :type context: behave.runner.Context
    """
    pass


@given("rodbot is running")
def step_rodbot_running(context):
    """
    See if bot is running.
    NOTE: SO FAR JUST LAUNCH SCRIPT. IN THE FUTURE IT SHOULD BE A SERVICE AND THIS STEP SHOULD CHECK THAT THE SERVICE
    IS RUNNING
    :type context: behave.runner.Context
    """
    assert check_bot()


def check_bot():
    '''
    Function to check if bot is running OK.
    :return: boolean, True if running OK
    '''
    if sys.platform == 'win32':  # If we are in windows system
        import psutil
        pythons_processes = [" ".join(p.cmdline()) for p in psutil.process_iter() if p.name() in "python.exe"]
        if any('rodbot.py' in p for p in pythons_processes):
            return True
    else:  # If we are in linux system
        process_command = 'ps aux | grep python'
        process = subprocess.Popen(process_command, stdout=subprocess.PIPE, shell=True)
        output, dummy_error = process.communicate()
        if 'rodbot.py' in output:
            return True

    try:
        subprocess.Popen('python rodbot.py -x simulator'.split(), stdout=subprocess.PIPE)
        sleep(3)  # Wait till have a result from the bot. Maybe we could should substitute this for a wait_for
        return True
    except:
        return False


@given("there is access to api exchange")
def step_check_api_simulator_access(context):
    """
    Step to check that we can request to the Api of the simulator, if not try to launch it
    :type context: behave.runner.Context
    """
    try:
        logger.debug('Checking access to api exchange sim...')
        r = requests.get('http://127.0.0.1:9071/market/stats')
        assert r.status_code == 200, 'Api exchange simulator is not running properly'
    except requests.ConnectionError:
        logger.info('First attempt checking api exchange didnt get a valid 200 response.'
                    ' Launch api exchange simulator and checking again...')
        run_command = ('python ' + os.path.join('bdd', 'api_exchange_simulator', 'api_ex_sim.py')).split()
        subprocess.Popen(run_command, stdout=subprocess.PIPE)
        sleep(3)
        r = requests.get('http://127.0.0.1:9071/market/stats')
        if r.status_code != 200:
            logger.error('Api exchange simulator is not running properly')
        assert r.status_code == 200, 'Api exchange simulator is not running properly'


@then('.* can know the current "(?P<pair>\w{3,5}-\w{3,5})" volume')
def step_volume_is_valid(context, pair):
    """
    Step to check volume. Check that volume is as expected and also that is included in the list of volumes ordered.
    :type context: behave.runner.Context
    :param pair: Name of the pair in the form XXX-YYY
    """
    expected_volume = float(json.loads(API_EX_SIM_PAIRS_STATS)["result"][pair]["base_volume"])
    logger.debug('Expected volume: %s', expected_volume)
    with open(VOLUME_PAIRS_FILE, 'r') as f:
        pairs_volume_dict = json.load(f)

    check_time_volume(pairs_volume_dict)

    logger.debug('Pairs volumes: %s', pairs_volume_dict)

    assert expected_volume == pairs_volume_dict['pairs_volume'][pair],\
        'Error volume for {pair}: expected {expected}, current {current}'.format(
            pair=pair, expected=expected_volume, current=pairs_volume_dict['pairs_volume'][pair]
        )

    pairs_volume_sorted = dict(pairs_volume_dict['pairs_volume_sorted'])
    assert float(pairs_volume_sorted[pair]) >= 0,\
        'Error in volume for {pair}: {current} not expected volume'.format(pair=pair,
                                                                           current=pairs_volume_sorted[pair])


@then('.* can know the list of volumes in descending order')
def step_know_volume(context):
    """
    :type context: behave.runner.Context
    """
    with open(VOLUME_PAIRS_FILE, 'r') as f:
        pairs_volume_dict = json.load(f)

    check_time_volume(pairs_volume_dict)

    volumes = [v[1] for v in pairs_volume_dict['pairs_volume_sorted']]

    logger.debug('Pair volumes: %s', volumes)
    assert volumes == sorted(volumes, reverse=True), 'List of ordered volumes is not ok'


@then("Rodrigo can know what pairs don't have volume")
def step_know_no_volume(context):
    """
    :type context: behave.runner.Context
    """
    with open(VOLUME_PAIRS_FILE, 'r') as f:
        pairs_volume_dict = json.load(f)

    check_time_volume(pairs_volume_dict)

    logger.debug('Pairs volume: %s', pairs_volume_dict)
    assert set(pairs_volume_dict['pairs_withouth_volume']) == \
        set([k for k, v in pairs_volume_dict['pairs_volume'].iteritems() if v == 0])


def check_time_volume(pairs_volume):
    '''
    Function helper to check that time in rodbot output is a near time. The function does not return anything, it just
    does the checkings
    :param pairs_volume: dict with the output of rodbot
    '''
    time_request = datetime.strptime(pairs_volume['time'], '%Y-%m-%dT%H:%M:%S.%f')
    logger.debug('Time request: %s', time_request)
    assert (datetime.now() > time_request) and (datetime.now() - timedelta(minutes=10) < time_request), \
        'Time of the last request is not as expected: {} is not near now and 10 minutes before'.format(time_request)
