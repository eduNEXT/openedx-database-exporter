#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base import OperationError
from truncate import Truncate
from drop import Drop
from erode import Erode


def get_operation_for_table(cnx, table_name):
    """
        Valid operations:
        - truncate
        - erode_by_
        - drop
    """
    target = []

    # The highest precedence
    if Erode.is_erode_required(cnx, table_name):
        target.append(Erode(cnx=cnx, table_name=table_name))

    if Truncate.is_truncate_required(cnx, table_name):
        target.append(Truncate(cnx=cnx, table_name=table_name))

    # The lowest precedence
    if Drop.is_drop_required(cnx, table_name):
        target.append(Drop(cnx=cnx, table_name=table_name))

    # We can reduce all the operations to a subset of only the required. e.g. Drop  + Truncate = Drop

    if len(target) == 0:
        raise OperationError("Error at: {}. Every table must have at least one operation".format(table_name))
    return target


def get_all_tables(cnx):
    result = cnx.execute("""show tables""")
    key = "Tables_in_{}".format(cnx._db)
    return [k[key] for k in result]
