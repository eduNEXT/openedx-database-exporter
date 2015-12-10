#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from .. import settings
from .base import Operation


class Erode(Operation):
    """
    Erode
    """
    def __init__(self, operation, *args, **kwargs):
        self.type = 'Erode'

    def __call__(self):
        super(Operation)
        if self.erode_by_course:
            None
            # query_result = self.cnx.execute("""DELETE from %s where course_id in %s""", (self.table_name,course_list))
        if self.erode_by_user:
            None
            # query_result = self.cnx.execute("""DELETE from %s where user_id in %s""", (self.table_name,user_list))
        if self.other_delete:
            None
            # query_result = self.cnx.execute("""DELETE from %s where %s in %s""", (self.table_name, self.column_name, self.eroder_list))
        # return query_result

    @staticmethod
    def is_erode_required(cnx, table_name):
        # TODO

        return False
