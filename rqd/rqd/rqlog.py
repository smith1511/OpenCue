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
       Logs to /var/log/messages"""

    # Always setup the default logging for console and syslog
    logging.config.dictConfig(logs.configs.DEFAULT_LOGGING)

    if os.path.isfile(rqconstants.LOGGING_CONFIG_FILE):
        
        config = None
        logging.info('Configuring logging from config file %s' % (rqconstants.LOGGING_CONFIG_FILE))

        try:
            # Setup user specified logging
            with open(rqconstants.LOGGING_CONFIG_FILE) as f:
                #config = json.load(f)
                s = f.read()
                config = ast.literal_eval(s)
        except Exception, e:
            logging.error("Failed to read logging config file %s due to %s at %s" % (rqconstants.LOGGING_CONFIG_FILE, e, traceback.extract_tb(sys.exc_info()[2])))  

        try:
            logging.config.dictConfig(config)
        except Exception, e:
            logging.error("Failed to load logging config file %s due to %s at %s" % (rqconstants.LOGGING_CONFIG_FILE, e, traceback.extract_tb(sys.exc_info()[2])))  

    logging.info('Logging setup completed')
