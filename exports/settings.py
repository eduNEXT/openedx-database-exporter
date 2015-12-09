#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

# Add settings here
MY_OPTION = "hola"


# Settings for the operations module

FORCED_TRUNCATE = [
***REMOVED***
***REMOVED***
]
***REMOVED***
    '^microsite_configuration.+'
]


# Settings for the preprocess module

MICROSITE = "***REMOVED***"
MICROSITE_ORGS_4_USERS = [***REMOVED***]
MICROSITE_ORGS_4_COURSES = [***REMOVED***]


# Settings for the databases module

DB_DATABASE = "edxapp"
DB_USER = "root"
DB_PASSWD = ""
DB_HOST = "localhost"

try:
    from .private import *      # pylint: disable=import-error
except ImportError:
    pass

logging.basicConfig(level=logging.WARNING)
