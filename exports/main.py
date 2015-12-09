#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings
from databases.mysql import Connection
import preprocessing.user_list as user_lister
import preprocessing.course_list as course_lister


def main():
    """
    Entry point for our application
    """


    print "Starting erode process..."
    print "Setting up connection to {}@{}".format(settings.DB_DATABASE, settings.DB_HOST)
    cnx = Connection(
        db=settings.DB_DATABASE,
        user=settings.DB_USER,
        passwd=settings.DB_PASSWD,
        host=settings.DB_HOST
    )


    microsite_orgs = settings.MICROSITE_ORGS_4_USERS
    microsite_url = settings.MICROSITE

    users_list = user_lister.get_users_list(cnx, microsite_url, microsite_orgs)
    print "First 5 user ids:{}".format(users_list[:5])
    users_list.sort()
    print users_list[:15]

    microsite_orgs = settings.MICROSITE_ORGS_4_COURSES

    print ""

    courses_list = course_lister.get_courses_list(cnx, microsite_url, microsite_orgs)
    print "First 5 course ids:{}".format(courses_list[:5])

    query_result = cnx.execute(
                               """SELECT * FROM auth_user WHERE id in %s""",
                               (users_list[:5],)
                              )
    print ""
    for row in query_result:
        print "{} {} {}".format(row['id'], row['username'], row['email'])
    cnx.close()
