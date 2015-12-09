#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings
from databases.mysql import Connection
import erode_inputs.user_list as user_lister


def main():
    """
    Entry point for our application
    """
    db_database = "edxapp"
    db_user = "edxapp001"
    db_passwd = "edxapp"
    db_host = "192.168.0.195"

    print "Starting erode process..."
    print "Setting up connection to {}@{}".format(db_database, db_host)
    cnx = Connection(
        db=db_database,
        user=db_user,
        passwd=db_passwd,
        host=db_host
    )
    print "Getting user list for {} ...".format(settings.MICROSITE)

    microsite_orgs = settings.MICROSITE_ORGS
    microsite_url = settings.MICROSITE

    users_list = user_lister.get_users_list(cnx, microsite_url, microsite_orgs)
    print "First 5 user ids:{}".format(users_list[:5])

    cnx.close()
