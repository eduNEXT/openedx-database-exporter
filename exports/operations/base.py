#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from .. import settings


class Operation(object):
    """
    The operation class defines a callable that carries out a set of sql
    commands to process a table.
    """

    def __init__(self, *args, **kwargs):
        self.dry_run = True
        self.color = "\033[35m"
        if kwargs.get('table_name', False):
            self.table_name = kwargs.get('table_name')
        if kwargs.get('cnx', False):
            self.cnx = kwargs.get('cnx')
        else:
            # Eventually we should create a new connection
            raise Exception('The operation requires a connection')

    def __call__(self):
        print "executing: {}".format(self.type)

    def __unicode__(self):
        return u"<Operation: {}{}\033[00m> on Table: {}".format(self.color, type(self).__name__, self.table_name)

    def __repr__(self):
        return unicode(self)


class OperationError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "\033[91m{}\033[00m".format(self.msg)


def is_erode_required(cnx, table_name):
    # TODO

    return False

