#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base import OperationError, Operation
from truncate import Truncate
from drop import Drop
from erode import Erode
from noop import Noop


def get_parent_ops(cnx, table_name):
    """
    Things to be eroded:
    """
    target = []

    parents = cnx.execute(
        """
        SELECT * FROM information_schema.KEY_COLUMN_USAGE
        WHERE REFERENCED_TABLE_NAME = %s
        """,
        (table_name,)
    )

    for parent in parents:
        target.append(Operation('evaluate_parent_{}'.format(parent['TABLE_NAME']), cnx=cnx, table_name=table_name))

    return target


def add_operations(op1, op2):
    # FIXME, this is not solid enough
    if isinstance(op2, Drop):
        return op2

    if isinstance(op2, Truncate):
        return op2

    # We cant reduce other operations
    if isinstance(op1, tuple):
        return op1 + (op2,)
    else:
        return (op1, op2,)


def get_operation_for_table(cnx, table_name):
    """
        Valid operations:
        - truncate
        - erode_by_
        - drop
    """
    target = []

    # The highest precedence
    erodes = Erode.get_all(cnx, table_name)
    for erode_operation in erodes:
        target.append(erode_operation)

    if Truncate.is_required(cnx, table_name):
        target.append(Truncate(cnx=cnx, table_name=table_name))

    # The lowest precedence
    if Drop.is_required(cnx, table_name):
        target.append(Drop(cnx=cnx, table_name=table_name))

    if Noop.is_required(cnx, table_name):
        target.append(Noop(cnx=cnx, table_name=table_name))

    # This is costly to calculate, so we only do it if there is no previous operations
    if len(target) == 0:
        ops = get_parent_ops(cnx, table_name)
        for parent_operation in ops:
            target.append(parent_operation)

    # We can reduce all the operations to a subset of only the required. e.g. Drop  + Truncate = Drop
    target = reduce(add_operations, target)
    if not isinstance(target, tuple):
        target = (target,)

    # We can make this a FailOperation
    if len(target) == 0:
        raise OperationError("Error at: {}. Every table must have at least one operation".format(table_name))

    return target


def get_all_tables(cnx):
    result = cnx.execute("""show tables""")
    key = "Tables_in_{}".format(cnx._db)
    return [k[key] for k in result]
