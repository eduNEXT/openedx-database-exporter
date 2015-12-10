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
    def is_required(cnx, table_name):
        # TODO

        return False