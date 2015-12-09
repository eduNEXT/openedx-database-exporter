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


def get_all_tables(cnx):
    result = cnx.execute("""show tables""")
    key = "Tables_in_{}".format(cnx._db)
    return [k[key] for k in result]


def is_erode_required(cnx, table_name):
    # TODO

    return False


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


def get_operation_for_table(cnx, table_name):
    """
        Valid operations:
        - truncate
        - erode_by_
        - drop
    """
    target = []

    # The highest precedence
    if is_erode_required(cnx, table_name):
        target.append(Operation('erode_by_something', cnx=cnx))

    if is_truncate_required(cnx, table_name):
        target.append(Operation('truncate', cnx=cnx))

    # The lowest precedence
    if is_drop_required(cnx, table_name):
        target.append(Operation('drop', cnx=cnx))

    # We can reduce all the operations to a subset of only the required. e.g. Drop  + Truncate = Drop

    if len(target) == 0:
        raise OperationError("Error at: {}. Every table must have at least one operation".format(table_name))
    return target
