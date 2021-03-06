#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import chain

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
    color = "\033[34m"
    priority = 40

    def __init__(self, *args, **kwargs):
        super(Erode, self).__init__(*args, **kwargs)
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

            if isinstance(obj, list):
                # Join a list of dicts to support the same operation more than once
                iteritems = []
                for item in obj:
                    iteritems.append(item.iteritems())

                iterator = chain.from_iterable(iteritems)
            else:
                # Regular iterator with only one dict
                iterator = obj.iteritems()

            for classname, extras in iterator:
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

        return target

    def __unicode__(self):
        return u"<Operation: {}{} by {}\033[00m> on Table: {}".format(self.color, self.get_name(), self.column_name, self.table_name)


class ErodeByParent(Erode):
    """
    """
    priority = 50

    def __init__(self, *args, **kwargs):
        super(Erode, self).__init__(*args, **kwargs)

        self.column_name = kwargs.get('column_name')
        self.uses = kwargs.get('uses')
        self.parent = kwargs.get('parent')

        self.child_id = kwargs.get('child_id', 'id')
        self.parent_id = kwargs.get('parent_id', 'id')

        # This is probably empty
        self.eroder_list = kwargs.get('eroder_list')

        if self.child_id == self.parent_id == 'id':
            raise Exception("""Eroding with both parent and child ids as 'id' is not really cool.
                Check your configuration for table {}""".format(self.table_name))

    def __call__(self):

        prepared_query = """DELETE
        FROM {table_name}
        WHERE {child_id} IN (
            SELECT {parent_id}
            from {parent_table}
            where {column_name} not in %s
        )""".format(
            table_name=self.table_name,
            child_id=self.child_id,
            parent_id=self.parent_id,
            parent_table=self.parent,
            column_name=self.column_name,
        )

        self.fill_eroder_list()
        query_result = self.cnx.execute(prepared_query, (self.eroder_list,), dry_run=self.dry_run)
        return query_result

    def __unicode__(self):
        return u"<Operation: {}{} by {}\033[00m> on Table: {}".format(
            self.color, self.get_name(), self.column_name, self.table_name
        )


class ErodeByAppName(Erode):
    """
    This is a fixed migration to remove the rows on the south_migrationhistory table
    that belong to our internal operation
    """

    def __init__(self, *args, **kwargs):
        super(ErodeByAppName, self).__init__(*args, **kwargs)
        self.apps_to_delete = kwargs.get('apps', ['microsite_configuration'])

    def __call__(self):
        query_string = """DELETE FROM {table_name} WHERE {column_name} in %s""".format(
            table_name=self.table_name,
            column_name=self.column_name,
        )
        query_result = self.cnx.execute(query_string, (self.apps_to_delete,), dry_run=self.dry_run)
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
            ErodeHelper.users_list.sort()
        return ErodeHelper.users_list

    @staticmethod
    def get_courses_list(cnx):
        if not ErodeHelper.courses_list:
            ErodeHelper.courses_list = course_list.get_courses_list(cnx, ErodeHelper.host_name, ErodeHelper.org_list_courses)
        return ErodeHelper.courses_list

    @staticmethod
    def get_other_list(args):
        None
