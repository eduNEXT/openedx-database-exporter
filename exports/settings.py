#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


# Settings for the operations module

FORCED_ERODE = {
    'auth_user': {'Erode': {'uses': 'user_list', 'column_name': 'id'}},
    'south_migrationhistory': {'ErodeSouthMigration': {}},
    'course_groups_coursecohort': {
        'ErodeByParent': {
            'column_name': 'course_id',
            'uses': 'course_list',
            'parent': 'course_groups_courseusergroup',
            'child_id': 'course_user_group_id',
        }
    },
    'courseware_studentmodulehistory': {
        'ErodeByParent': {
            'column_name': 'student_id',
            'uses': 'user_list',
            'parent': 'courseware_studentmodule',
            'child_id': 'student_module_id',
        }
    },
    'courseware_xmodulestudentinfofield': {
        'Erode': {
            'uses': 'user_list',
            'column_name': 'student_id',
        }
    },
    'courseware_xmodulestudentprefsfield': {
        'Erode': {
            'uses': 'user_list',
            'column_name': 'student_id',
        }
    },
    'workflow_assessmentworkflowstep': {
        'ErodeByParent': {
            'column_name': 'course_id',
            'uses': 'course_list',
            'parent': 'workflow_assessmentworkflow',
            'child_id': 'workflow_id',
        }
    },
    'django_comment_client_permission_roles': {
        'ErodeByParent': {
            'column_name': 'course_id',
            'uses': 'course_list',
            'parent': 'django_comment_client_role',
            'child_id': 'role_id',
        }
    },
    'student_manualenrollmentaudit': {
        'Erode': {
            'uses': 'user_list',
            'column_name': 'enrolled_by_id',
        }
    },
    'submissions_scoresummary': {
        'ErodeByParent': {
            'column_name': 'course_id',
            'parent': 'submissions_studentitem',
            'uses': 'course_list',
            'child_id': 'student_item_id',
        }
    },
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
