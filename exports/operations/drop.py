#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import base
from .. import settings


class Drop(base.Operation):
    """
    Drop
    """

    def __init__(self, *args, **kwargs):
        self.type = 'Drop'

    def __call__(self):
        super(base.Operation)
        # query_result = self.cnx.execute("""DROP TABLE %s""", (self.table_name,))
        return query_result

    @staticmethod
    def is_drop_required(cnx, table_name):
        """
        Things to be dropped:
            Anything matching a list of regex stored in settings.FORCED_DROP
        """
        combined = "(" + ")|(".join(settings.FORCED_DROP) + ")"
        if re.match(combined, table_name):
            return True

        # Finally, this table is not to be dropped
        return False
