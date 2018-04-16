# import logging
# from logging.config import dictConfig
# import os
#
#
# TRADING_LOG = os.path.join('log', 'rodbot.{}')
#
#
# dict_log_config = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "standard": {
#             "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
#         },
#     },
#     "handlers": {
#         "console": {
#             "level":"INFO",
#             "class":"logging.StreamHandler",
#             "formatter": "standard"
#         },
#         "file_debug": {
#             "level":"DEBUG",
#             "class":"logging.FileHandler",  # Other option might be logging.handlers.RotatingFileHandler
#             "formatter": "standard",
#             "filename": TRADING_LOG.format('debug')
#         },
#         "file_info": {
#             "level": "INFO",
#             "class": "logging.FileHandler",
#             "formatter": "standard",
#             "filename": TRADING_LOG.format('info')
#         },
#         "file_error": {
#             "level": "ERROR",
#             "class": "logging.FileHandler",
#             "formatter": "standard",
#             "filename": TRADING_LOG.format('error')
#         }
#     },
#     "loggers": {
#         "": {
#             "handlers": ["console", "file_debug", "file_info", "file_error"],
#             "level": "INFO",
#             "propagate": True
#         }
#     }
# }
# dictConfig(dict_log_config)
# logger = logging.getLogger(__name__)