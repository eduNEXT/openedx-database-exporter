#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from .. import settings


class Operation(object):
    """
    The operation class defines a callable that carries out a set of sql
    commands to process a table.
    """

    def __init__(self, operation, *args, **kwargs):
        self.type = operation


        if kwargs.get('cnx', False):
            self.cnx = kwargs.get('cnx')
        else:
            # Eventually we should create a new connection
            raise Exception('The operation requires a connection')

    def __call__(self):
        # TODO: either define here based on the type or extend this class and
        # implement there
        print "executing: {}".format(self.type)

    def __unicode__(self):
        colors = {
            "trun": "\033[36m",
            "erod": "\033[34m",
            "drop": "\033[33m",
        }
        color = colors.get(self.type[:4], "\033[35m")
        return u"<Operation: {}{}\033[00m>".format(color, self.type)

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

