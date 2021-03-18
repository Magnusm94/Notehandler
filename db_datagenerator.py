#!/usr/bin/env python

import json
import sys
import os


if __name__ == "__main__":
    login = \
    {
    "database": "mynotes",
    "user": sys.argv[1],
    "password": "",
    "host": "localhost",
    "port": "5432"
    }
    with open(os.path.dirname(__file__) + '/notehandler/login.json', 'w') as outfile:
        json.dump(login, outfile, indent=4)
