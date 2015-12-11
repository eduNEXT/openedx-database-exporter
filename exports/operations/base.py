#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .. import settings


class Operation(object):
    """
    The operation class defines a callable that carries out a set of sql
    commands to process a table.
    """
    color = "\033[31m"
    priority = 0

    def __init__(self, *args, **kwargs):
        self.dry_run = settings.GLOBAL_DRY_RUN

        if kwargs.get('table_name', False):
            self.table_name = kwargs.get('table_name')

        if kwargs.get('name', False):
            self.name = kwargs.get('name')

        self.priority = kwargs.get('priority', self.priority)

        if kwargs.get('cnx', False):
            self.cnx = kwargs.get('cnx')
        else:
            # Eventually we should create a new connection
            raise Exception('The operation requires a connection')

    def __call__(self):
        print "executing: {}".format(self.get_name())

    def __unicode__(self):
        return u"<Operation: {}{}\033[00m> on Table: {}".format(self.color, self.get_name(), self.table_name)

    def __repr__(self):
        return unicode(self)

    def get_name(self):
        if hasattr(self, 'name'):
            return self.name
        else:
            return type(self).__name__


class OperationError(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return "\033[91m{}\033[00m".format(self.msg)
