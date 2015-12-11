#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from .base import Operation
from .. import settings


class Noop(Operation):
    """
    No Operation
    """
    color = "\033[32m"

    def __init__(self, *args, **kwargs):
        super(Noop, self).__init__(*args, **kwargs)

    def __call__(self):
        super(Operation)
        return True

    @staticmethod
    def is_required(cnx, table_name):
        """
        Things to be left alone:
            Anything matching a list of regex stored in settings.FORCED_NOOP
        """
        combined = "(" + ")|(".join(settings.FORCED_NOOP) + ")"
        if re.match(combined, table_name):
            return True

        return False
