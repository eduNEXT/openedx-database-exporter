#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import settings
from ..preprocessing import user_list
from ..preprocessing import course_list

from .base import Operation


class Erode(Operation):
    """
    Erode
    """
    LIST_OF_USERS = 'user_list'
    LIST_OF_COURSES = 'course_list'

    def __init__(self, *args, **kwargs):
        super(Erode, self).__init__(*args, **kwargs)
        self.color = "\033[34m"
        self.column_name = kwargs.get('column_name')
        self.uses = kwargs.get('uses')
        if kwargs.get('eroder_list', False):
            self.eroder_list = kwargs.get('eroder_list')

    def __call__(self):
        # assert that there is an eroder_list
        self.fill_eroder_list()
        query_string = """DELETE from {} WHERE {} NOT IN %s""".format(self.table_name, self.column_name)
        query_result = self.cnx.execute(query_string, (self.eroder_list,), dry_run=self.dry_run)
        return query_result

    def fill_eroder_list(self):
        if self.uses == Erode.LIST_OF_COURSES:
            self.eroder_list = ErodeHelper.get_courses_list(self.cnx)
        if self.uses == Erode.LIST_OF_USERS:
            self.eroder_list = ErodeHelper.get_users_list(self.cnx)

    @classmethod
    def get_all(cls, cnx, table_name):
        """
        Things to be eroded:
            Tables that contain a course_id column
            Tables that contain a user_id column
        """
        target = []

        settings.FORCED_ERODE
        if table_name in settings.FORCED_ERODE.keys():
            obj = settings.FORCED_ERODE.get(table_name)
            for classname, extras in obj.iteritems():
                try:
                    op = globals()[classname]
                    target.append(op(cnx=cnx, table_name=table_name, **extras))
                except KeyError:
                    target.append(Operation(name='Missing Operation Definition: {}'.format(classname), cnx=cnx, table_name=table_name))

        if len(target) == 0:
            result = cnx.execute(
                """
                SELECT * FROM information_schema.columns
                where TABLE_SCHEMA = %s and TABLE_NAME = %s
                """,
                ('edxapp', table_name)
            )
            for row in result:
                if row.get('COLUMN_NAME') == 'course_id':
                    target.append(Erode(uses=cls.LIST_OF_COURSES, cnx=cnx, table_name=table_name, column_name='course_id'))

                if row.get('COLUMN_NAME') == 'course_key':
                    target.append(Erode(uses=cls.LIST_OF_COURSES, cnx=cnx, table_name=table_name, column_name='course_key'))

                # TODO: we should filter better whether a user_id column_name really is what it shoudl be. E.g. to be foreing_key
                if row.get('COLUMN_NAME') == 'user_id':
                    target.append(Erode(uses=cls.LIST_OF_USERS, cnx=cnx, table_name=table_name, column_name='user_id'))

                # TODO: we should filter better whether a user_id column_name really is what it shoudl be. E.g. to be foreing_key
                if row.get('COLUMN_NAME') == 'user_profile_id':
                    target.append(Operation(name='erode_by_user_profile_id', cnx=cnx, table_name=table_name))

        return target

    def __unicode__(self):
        return u"<Operation: {}{} by {}\033[00m> on Table: {}".format(self.color, self.get_name(), self.column_name, self.table_name)


class ErodeSouthMigration(Erode):
    """
    This is a fixed migration to remove the rows on the south_migrationhistory table
    that belong to our internal operation
    """

    def __call__(self):
        query_string = """DELETE FROM south_migrationhistory WHERE app_name = %s"""
        query_result = self.cnx.execute(query_string, ('microsite_configuration',), dry_run=self.dry_run)
        return query_result

    def __unicode__(self):
        return u"<Operation: {}{}\033[00m>".format(self.color, self.get_name())



class ErodeHelper():
    """Helper class that obtains the needed lists for erode"""
    users_list = None
    courses_list = None
    host_name = settings.MICROSITE_HOSTNAME
    org_list_users = settings.MICROSITE_ORGS_4_USERS
    org_list_courses = settings.MICROSITE_ORGS_4_COURSES

    @staticmethod
    def get_users_list(cnx):
        if not ErodeHelper.users_list:
            ErodeHelper.users_list = user_list.get_users_list(cnx, ErodeHelper.host_name, ErodeHelper.org_list_users)
        return ErodeHelper.users_list

    @staticmethod
    def get_courses_list(cnx):
        if not ErodeHelper.courses_list:
            ErodeHelper.courses_list = course_list.get_courses_list(cnx, ErodeHelper.host_name, ErodeHelper.org_list_courses)
        return ErodeHelper.courses_list

    @staticmethod
    def get_other_list(args):
        None
