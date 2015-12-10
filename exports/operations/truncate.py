#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from .base import Operation
from .. import settings


class Truncate(Operation):
    """
    Truncate
    """

    def __init__(self, *args, **kwargs):
        self.type = 'Truncate'

    def __call__(self):
        super(Operation)
        # query_result = self.cnx.execute("""TRUNCATE TABLE %s""", (self.table_name,))
        # return query_result

    @staticmethod
    def is_truncate_required(cnx, table_name):
        """
        Things to be truncated:
            All empty tables
            Anything matching a list of regex stored in settings.FORCED_TRUNCATE
        """
        # Some tables must be Forced to be Truncated
        combined = "(" + ")|(".join(settings.FORCED_TRUNCATE) + ")"
        if re.match(combined, table_name):
            return True

        # Tables with 0 records are trunctated to make sure the autoincrement will also be reset
        # TODO: we have to sanitize this on our own
        result = cnx.execute("""SELECT count(*) FROM {table_name}""".format(table_name=table_name))
        if result[0]['count(*)'] == 0:
            return True

        # Finally, this table is not suited for truncation
        return False
