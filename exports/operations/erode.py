#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import settings
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
        query_result = self.cnx.execute("""DELETE from %s WHERE %s IN %s""", (self.table_name, self.column_name, self.eroder_list), dry_run=self.dry_run)
        return query_result

    def setErodeVariables(self, column_name, eroder_list):
        self.column_name = column_name
        self.eroder_list = eroder_list

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
            extras = settings.FORCED_ERODE.get(table_name)
            target.append(Erode(cnx=cnx, table_name=table_name, **extras))

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
                    target.append(Operation('erode_by_user_profile_id', cnx=cnx, table_name=table_name))

        return target

    def __unicode__(self):
        return u"<Operation: {}{} by {}\033[00m> on Table: {}".format(self.color, self.get_name(), self.column_name, self.table_name)
