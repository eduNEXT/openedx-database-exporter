#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools import *

# Courses with enrroled students + ...


def get_courses_with_enrolled_students(cnx, org_list):
    """
    Courses from the given orgs that have enrolled students
    """
    regex = org_regex(org_list)
    query_result = cnx.execute(
                               """SELECT DISTINCT(course_id) FROM student_courseenrollment WHERE course_id REGEXP %s""",
                               (regex,)
                              )

    print "    CE: There are {} courses with enrolled students from this orgs:{}".format(len(query_result), org_list)
    return query_result


def get_courses_list(cnx, site, org_list):
    """
    Total courses of a microsite
    """
    # EnS = get_empty_users_recoverable(cnx, site)
    courses_from_enrolment = get_courses_with_enrolled_students(cnx, org_list)
    courses_list = courses_from_enrolment #+ ..
    print "courses: There are {} courses for {} with orgs:{}".format(len(courses_list), site, org_list)
    return courses_list
