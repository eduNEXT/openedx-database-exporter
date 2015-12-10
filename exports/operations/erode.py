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
        query_result = self.cnx.execute("""DELETE from %s where %s in %s""", (self.table_name, self.column_name, self.eroder_list), dry_run=self.dry_run)
        return query_result

    def setErodeVariables(self, column_name, eroder_list):
        self.column_name = column_name
        self.eroder_list = eroder_list

    @staticmethod
    def is_erode_required(cnx, table_name):
        # TODO

        return False
