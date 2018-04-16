'''
File to configure the environment for the behave's tests.
'''

# from behave import *
import logging
from logging.config import dictConfig
import os


LOG_FILE = os.path.join('bdd', 'logs', 'behave.log')


dict_log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "file_debug": {
            "level": "DEBUG",
            "class": "logging.FileHandler",  # Other option might be logging.handlers.RotatingFileHandler
            "formatter": "standard",
            "filename": LOG_FILE
        },
        "file_info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": LOG_FILE
        },
        "file_error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "formatter": "standard",
            "filename": LOG_FILE
        }
    },
    "loggers": {
        "": {
            "handlers": ["file_debug"],
            "level": "DEBUG",
            "propagate": True
        }
    }
}

dictConfig(dict_log_config)
logger = logging.getLogger('behave')


def before_all(context):
    """
    Settings to execute before all tests
    """
    log_level = logging.DEBUG if 'verbose' in context.config.userdata else logging.INFO
    logger.setLevel(log_level)

    logger.info("Before_all starts")
    logger.info("Before_all Ends")


def before_feature(context, feature):
    """
    Settings to execute before a feature (a feature file)
    @param context: execution context
    @param feature: feature
    """
    logger.info('Running feature: %s', feature)


def before_tag(context, tag):
    """
    Is executed before the test for each tag that describes it
    @param context: Context variables
    @param tag: tag to be analyzed. It only includes one and
               only one tag if specified before the test
    """
    pass


def before_scenario(context, scenario):
    """
    Is executed before each scenario
    @param context: Context variables
    @param scenario: Scenario being executed
    """
    logger.info('Running scenario: %s', scenario)


def before_step(context, step):
    """
    Is executed before each step
    @param context: Context variables
    @param step: step being executed
    """
    logger.info('Running step: %s', step)


def after_tag(context, tag):
    """
    Is executed after the test for each tag that describes it
    @param context Context variables
    @param tag tag to be analyzed. It only includes one and
           only one tag if specified before the test
    """
    pass


def after_step(context, step):
    """
    Is executed after each step
    @param context: Context variables
    @param step: step executed
    """
    if step.status == 'failed':
        logger.error('Error in step %s', step)


def after_scenario(context, scenario):
    """
    Is executed after each scenario
    @param context: Context variables
    @param scenario: Scenario executed
    """
    pass


def after_feature(context, feature):
    """
    Settings to execute after a feature (a feature file)
    @param context: execution context
    @param feature: feature
    """
    pass


def after_all(context):
    """
    Settings to execute before all tests
    @param context: execution context
    """
    logger.info('Finished')
