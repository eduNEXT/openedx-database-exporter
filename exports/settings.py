#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


# Settings for the operations module

FORCED_ERODE = {
    'auth_user': {'Erode': {'uses': 'user_list', 'column_name': 'id'}},
    'south_migrationhistory': {'ErodeSouthMigration': {}},
    'course_groups_coursecohort': {'ErodeByParent': {'column_name': 'course_id', 'parent': 'to_be_determined', 'uses': 'course_list'}},
    'courseware_studentmodulehistory': {'ErodeByParent': {'column_name': 'user_id', 'parent': 'to_be_determined', 'uses': 'user_list'}},
    'courseware_xmodulestudentinfofield': {'Erode': {'uses': 'user_list', 'column_name': 'student_id'}},
    'courseware_xmodulestudentprefsfield': {'Erode': {'uses': 'user_list', 'column_name': 'student_id'}},
    'workflow_assessmentworkflowstep': {'ErodeByParent': {'column_name': 'course_id', 'parent': 'workflow_assessmentworkflow', 'uses': 'course_list'}},
    'django_comment_client_permission_roles': {'ErodeByParent': {'column_name': 'course_id', 'parent': 'django_comment_client_role', 'uses': 'course_list'}},
    'student_manualenrollmentaudit': {'ErodeByParent': {'column_name': 'user_id', 'parent': 'student_courseenrollment', 'uses': 'user_list'}},   # Some data might be lost when the initial state was unenrolled
    'submissions_scoresummary': {'ErodeByParent': {'column_name': 'course_id', 'parent': 'submissions_studentitem', 'uses': 'course_list'}},
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

GLOBAL_DRY_RUN = False

# Settings for the preprocess module

MICROSITE_HOSTNAME = "***REMOVED***"
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
