#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools import *
import logging

logger = logging.getLogger(__name__)
# List of Users:

# Variables: Org list, Site url type Name

# ***REMOVED***
# ***REMOVED***
# ***REMOVED***
# Sites: SELECT user_id FROM edxapp.student_usersignupsource where site='***REMOVED***';

# Users of only this microsite = P-N
# Empty users recoverable = E n S

# Total users of a microsite= Users of only this microsite U Empty users recoverable


def positive_users_from_enrollment(cnx, org_list):
    """
    Positive: select distinct(user_id) from student_courseenrollment where course_id REGEXP '(course-v1:|^)(***REMOVED***)[+/]';
    """
    regex = org_regex(org_list)
    query_result = cnx.execute(
                               """SELECT DISTINCT(user_id) FROM student_courseenrollment WHERE course_id REGEXP %s""",
                               (regex,)
                              )

    logger.debug("        P: There are {} users in courses from this orgs:{}".format(len(query_result), org_list))
    return query_result


def negative_users_from_enrollment(cnx, org_list):
    """
    Negative: select distinct(user_id) from student_courseenrollment where course_id NOT REGEXP '(course-v1:|^)(***REMOVED***)[+/]';
    """
    regex = org_regex(org_list)
    query_result = cnx.execute(
                               """SELECT DISTINCT(user_id) FROM student_courseenrollment WHERE course_id NOT REGEXP %s""",
                               (regex,)
                              )
    logger.debug("        N: There are {} users not in courses from this orgs:{}".format(len(query_result), org_list))
    return query_result


def not_enrolled_users(cnx):
    """
    ***REMOVED***
    """
    query_result = cnx.execute("""SELECT * FROM auth_user WHERE id not IN (SELECT DISTINCT(user_id) FROM student_courseenrollment)""")
    logger.debug("        E: There are {} users not enrroled in a course".format(len(query_result)))
    return query_result


def users_from_sites(cnx, site):
    """
    Sites: SELECT user_id FROM edxapp.student_usersignupsource where site='***REMOVED***';
    """
    query_result = cnx.execute("""SELECT user_id FROM edxapp.student_usersignupsource where site=%s""", (site,))
    logger.debug("        S: There are {} users for {}".format(len(query_result), site))
    return query_result


def get_empty_users_recoverable(cnx, site):
    """
    Empty users recoverable = E n S
    """
    E = query_tuple_to_list(not_enrolled_users(cnx), 'id')
    E.sort()
    logger.debug("        E: {}".format(E[:10]))
    S = query_tuple_to_list(users_from_sites(cnx, site), 'user_id')
    S.sort()
    logger.debug("        S: {}".format(S[:10]))
    EnS = intersect_list(E, S)
    logger.debug("    EnS: There are {} empty users recoverable for {}".format(len(EnS), site))
    EnS.sort()
    logger.debug("    EnS: {}".format(EnS[:10]))
    return EnS


def get_site_only_users(cnx, org_list):
    """
    Microsite only users = P-N
    """

    P = query_tuple_to_list(positive_users_from_enrollment(cnx, org_list), 'user_id')
    P.sort()
    logger.debug("        P: {}".format(P[:10]))
    N = query_tuple_to_list(negative_users_from_enrollment(cnx, org_list), 'user_id')
    N.sort()
    logger.debug("        N: {}".format(N[:10]))
    PminusN = substract_list(P, N)
    logger.debug("    PminusN: There are {} users that are only in courses of these orgs: {}".format(len(PminusN), org_list))
    PminusN.sort()
    logger.debug("    PminusN: {}".format(PminusN[:10]))
    return PminusN


def get_users_list(cnx, site, org_list):
    """
    Total users of a microsite= Users of only this microsite U Empty users recoverable
    """
    EnS = get_empty_users_recoverable(cnx, site)
    PminusN = get_site_only_users(cnx, org_list)
    users = EnS + PminusN
    logger.debug("users: There are {} users for {} with orgs:{}".format(len(users), site, org_list))
    return users
