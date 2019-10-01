import os

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters':{
      'hostname': {
        '()': 'logs.filters.HostnameFilter'
      }
    },
    'formatters': {
      'simple': {
        'format': '%(asctime)s %(levelname)-9s %(hostname)s rqd3-%(module)-10s %(message)s'
      }
    },
    "handlers": {
        "console": {
            "class":     "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level":     "DEBUG",
            'formatter': 'simple',
        },
        "syslog": {
            "class":     "logging.handlers.SysLogHandler",
            "level":     "DEBUG",
            'formatter': 'simple',
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'syslog'],
            'filters': ['hostname'],
        }
    }
}

APP_INSIGHTS_LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters':{
      'hostname': {
        '()': 'logs.filters.HostnameFilter'
      }
    },
    'formatters': {
      'simple': {
        'format': '%(asctime)s %(levelname)-9s %(hostname)s rqd3-%(module)-10s %(message)s'
      }
    },
    "handlers": {
        "console": {
            "class":     "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "level":     "DEBUG",
            'formatter': 'simple',
        },
        "syslog": {
            "class":     "logging.handlers.SysLogHandler",
            "level":     "DEBUG",
            'formatter': 'simple',
        },
        "appinsights": {
            "class":     "applicationinsights.logging.LoggingHandler",
            "instrumentation_key":  "4dcab37a-38ad-4e15-bd4a-4cbc47b93f30",
            "level":     "DEBUG",
            'formatter': 'simple',
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', 'syslog', 'appinsights'],
            'filters': ['hostname'],
        }
    }
}

SPLUNK_LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters':{
      'hostname': {
        '()': 'logs.filters.HostnameFilter'
      }
    },
    'formatters': {
      'simple': {
        'format': '%(asctime)s %(levelname)-9s %(hostname)s rqd3-%(module)-10s %(message)s'
      }
    },
    'handlers': {
        'splunk': { # handler for splunk, level Warning. to not have many logs sent to splunk
            'level': 'WARNING',
            'class': 'splunk_logging_handler.SplunkLoggingHandler',
            'url': os.getenv('SPLUNK_HTTP_COLLECTOR_URL'),
            'splunk_key': os.getenv('SPLUNK_TOKEN'),
            'splunk_index': os.getenv('SPLUNK_INDEX'),
            'formatter': 'simple',
            'filters': ['filterForSplunk']
        },
        'console': { 
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'simple',
        },
    },
    'loggers': { # the logger, root is used
        '': {
            'handlers': ['console', 'splunk'],
            'level': 'DEBUG',
            'propagate': 'False', # does not give logs to other logers
            'filters': ['hostname'],
        }
    }
}