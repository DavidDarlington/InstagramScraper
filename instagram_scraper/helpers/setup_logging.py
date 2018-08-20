import os
import json
import logging.config


def setup_logging(
    default_file='logging.json',
    env_key='LOG_CFG',
    verbose=2,
    file_log_level=False
):
    """Configures the logger"""
    log_levels = ['ERROR', 'WARNING', 'INFO', 'DEBUG']

    path = os.path.join(os.path.dirname(__file__), '..', default_file)
    value = os.getenv(env_key, None)

    if value:
        path = value

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)

            if file_log_level is False:
                # Removes file logging handler if log level not specified
                config['handlers'].pop('file_handler', None)
                config['root']['handlers'].remove('file_handler')
            else:
                # Configures log level for file logging handler
                config['handlers']['file_handler']['level'] = log_levels[int(file_log_level)]

            # Configures log level for console logging handler
            config['handlers']['console']['level'] = log_levels[int(verbose)]

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)