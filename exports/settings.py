#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


# Settings for the operations module

FORCED_ERODE = {
    'auth_user': {'op': 'erode_by_user_id', 'column_name': 'id'},
    'south_migrationhistory': {'op': 'erode_south_migrationhistory'},
    'course_groups_coursecohort': {'op': 'erode_by_course_id_on_parent', 'parent': ''},
    'courseware_studentmodulehistory': {'op': 'erode_by_user_id_on_parent', 'parent': ''},
    'courseware_xmodulestudentinfofield': {'op': 'erode_by_user_id', 'column_name': 'student_id'},
    'courseware_xmodulestudentprefsfield': {'op': 'erode_by_user_id', 'column_name': 'student_id'},
    'workflow_assessmentworkflowstep': {'op': 'erode_by_course_id_on_parent', 'parent': 'workflow_assessmentworkflow'},
    'django_comment_client_permission_roles': {'op': 'erode_by_course_id_on_parent', 'parent': 'django_comment_client_role'},
    'student_manualenrollmentaudit': {'op': 'erode_by_user_id_on_parent', 'parent': 'student_courseenrollment'},  # Some data might be lost when the initial state was unenrolled
    'submissions_scoresummary': {'op': 'erode_by_course_id_on_parent', 'parent': 'submissions_studentitem'},
}
FORCED_TRUNCATE = [
    '^third_party_auth_oauth2providerconfig$',
    '^django_session$',
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
***REMOVED***
]
***REMOVED***
***REMOVED***
]
FORCED_NOOP = [
    '^embargo_country$',
    '^certificates_badgeimageconfiguration$',
***REMOVED***
***REMOVED***
***REMOVED***
]

GLOBAL_DRY_RUN = True

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
