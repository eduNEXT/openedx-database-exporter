#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

# Add settings here
MY_OPTION = "hola"
MICROSITE = "***REMOVED***"
MICROSITE_ORGS_4_USERS = [***REMOVED***]
MICROSITE_ORGS_4_COURSES = [***REMOVED***]


DB_DATABASE = "edxapp"
DB_USER = "root"
DB_PASSWD = ""
DB_HOST = "localhost"

try:
    from .private import *      # pylint: disable=import-error
except ImportError:
    pass

logging.basicConfig(level=logging.WARNING)
