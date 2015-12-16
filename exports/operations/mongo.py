#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import settings

from .erode import ErodeHelper


def cs_comments_service_erode(cnx, mysql_cnx=None):
    course_list = ErodeHelper.get_courses_list(mysql_cnx)
    user_list = ErodeHelper.get_users_list(mysql_cnx)

    # Mongo stores the ids as strings, so we need to convert them first
    user_id_str = [str(user) for user in user_list]

    # 1st collection
    result = cnx.remove(cnx.query_builder_in("course_id", course_list, negate=True), "contents")
    print result
    result = cnx.remove(cnx.query_builder_in("author_id", user_id_str, negate=True), "contents")
    print result

    # 2nd collection
    result = cnx.remove(cnx.query_builder_in("subscriber_id", user_id_str, negate=True), "subscriptions")
    print result

    # 3rd collection
    result = cnx.remove(cnx.query_builder_in("external_id", user_id_str, negate=True), "users")
    print result
