#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings
import logging
from databases.mysql import Connection
from operations.base import OperationError
import operations.utils as utils

logger = logging.getLogger(__name__)


def main():
    """
    Entry point for our application
    """
    logger.info("Setting up connection to {}@{}".format(settings.DB_DATABASE, settings.DB_HOST))
    cnx = Connection(dict_cursor=True)

    # Your CODE here
    all_ops = []
    for table_name in utils.get_all_tables(cnx):
        try:
            operations = utils.get_operation_for_table(cnx, table_name)
            for operation in operations:
                all_ops.append(operation)

        except OperationError, e:
            print "A Table lacks operations: \033[91m{}\033[00m".format(e.msg)

    # Sort and execute
    print "Executing Operations"
    cnx.execute("SET FOREIGN_KEY_CHECKS=0", dry_run=settings.GLOBAL_DRY_RUN)
    for op in all_ops:
        print op
        print "result: {}".format(op())
    cnx.execute("SET FOREIGN_KEY_CHECKS=1", dry_run=settings.GLOBAL_DRY_RUN)

    logger.info("Closing connection to DB")
    cnx.close()
