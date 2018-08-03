#!/usr/bin/python

import json
import logging


# INITIALIZE SETTINGS
def init():
    global config

    # OPEN CONFIGURATION FILE
    with open('../config.json', 'r') as f:
        config = json.load(f)

    # CONFIGURE LOGGING
    logging.basicConfig(
        filename=config['logging']['path'],
        level=logging.INFO
    )

    logging.info('Started')
