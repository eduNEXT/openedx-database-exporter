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
    operations = [Drop, Truncate, Erode]

    for operation in operations:
        if operation.is_required(cnx, table_name):
            target.append(operation(cnx=cnx, table_name=table_name))
            # break? because other operations are not needed?

    if len(target) == 0:
        raise OperationError("Error at: {}. Every table must have at least one operation".format(table_name))
    return target


def get_all_tables(cnx):
    result = cnx.execute("""show tables""")
    key = "Tables_in_{}".format(cnx._db)
    return [k[key] for k in result]
