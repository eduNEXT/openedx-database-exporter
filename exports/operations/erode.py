#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import settings
from .base import Operation


class Erode(Operation):
    """
    Erode
    """
    def __init__(self, *args, **kwargs):
        super(Erode, self).__init__(*args, **kwargs)
        self.color = "\033[34m"
        if kwargs.get('column_name', False):
            self.column_name = kwargs.get('column_name')
        if kwargs.get('eroder_list', False):
            self.eroder_list = kwargs.get('eroder_list')

    def __call__(self):
        query_result = self.cnx.execute("""DELETE from %s WHERE %s IN %s""", (self.table_name, self.column_name, self.eroder_list), dry_run=self.dry_run)
        return query_result

    def setErodeVariables(self, column_name, eroder_list):
        self.column_name = column_name
        self.eroder_list = eroder_list

    @staticmethod
    def get_all(cnx, table_name):
        """
        Things to be eroded:
            Tables that contain a course_id column
            Tables that contain a user_id column
        """
        target = []

        settings.FORCED_ERODE
        if table_name in settings.FORCED_ERODE.keys():
            obj = settings.FORCED_ERODE.get(table_name)
            target.append(Operation(obj.get('op'), cnx=cnx, table_name=table_name))

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
                    target.append(Operation('erode_by_course_id', cnx=cnx, table_name=table_name))

                if row.get('COLUMN_NAME') == 'course_key':
                    target.append(Operation('erode_by_course_id', cnx=cnx, table_name=table_name, column_name='course_key'))

                # TODO: we should filter better whether a user_id column_name really is what it shoudl be. E.g. to be foreing_key
                if row.get('COLUMN_NAME') == 'user_id':
                    target.append(Operation('erode_by_user_id', cnx=cnx, table_name=table_name))

                # TODO: we should filter better whether a user_id column_name really is what it shoudl be. E.g. to be foreing_key
                if row.get('COLUMN_NAME') == 'user_profile_id':
                    target.append(Operation('erode_by_user_profile_id', cnx=cnx, table_name=table_name))

        return target
