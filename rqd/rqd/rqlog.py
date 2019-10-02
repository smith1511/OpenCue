import json
import logging.config
import os
import sys
import traceback

import rqconstants
import logs.configs

import ast


def setupLogging():
    """Sets up the logging for RQD.
       Defaults logs to console and /var/log/messages"""

    # Always setup default logging for console and syslog
    logging.config.dictConfig(logs.configs.DEFAULT_LOGGING)

    if os.path.isfile(rqconstants.LOGGING_CONFIG_FILE):
        config = None
        logging.info('Configuring logging from config file {}'.format(rqconstants.LOGGING_CONFIG_FILE))

        try:
            # Setup user specified logging
            with open(rqconstants.LOGGING_CONFIG_FILE) as f:
                s = f.read()
                config = ast.literal_eval(s)
        except Exception, e:
            logging.error('Failed to read logging config file {} due to {} at {}'.format(rqconstants.LOGGING_CONFIG_FILE, e, traceback.extract_tb(sys.exc_info()[2])))

        if config:
            try:
                logging.config.dictConfig(config)
            except Exception, e:
                logging.error('Failed to load logging config file {} due to {} at {}'.format(rqconstants.LOGGING_CONFIG_FILE, e, traceback.extract_tb(sys.exc_info()[2])))

    logging.info('Logging setup completed')
