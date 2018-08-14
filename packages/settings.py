#!/usr/bin/python

import json


# INITIALIZE SETTINGS
def init():
    global config

    # OPEN CONFIGURATION FILE
    with open('../config.json', 'r') as f:
        config = json.load(f)
