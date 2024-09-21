import logging.config


logger_config = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'std_format': {
            'format': '%(levelname)s:\t[%(asctime)s] %(name)s - %(module)s:%(funcName)s:%(lineno)s \"%(message)s\"'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'std_format',
        },
        'rotating_files': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'std_format',
            'filename': 'debug.log',
            'maxBytes': 2000,
            'backupCount': 5
        },
    },
    'loggers': {
        'backend': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False
        }
    },

}

def init_logger():
    logging.config.dictConfig(logger_config)