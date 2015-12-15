#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings
import logging
import operator
from databases.mysql import Connection
from databases.mongo import Connection as MongoConnection
from operations.base import OperationError
import operations.utils as utils

logger = logging.getLogger(__name__)


def main():
    mongo_process()


def mongo_process():
    course_list = ["Scarchivistas/SGDISO/2014", "Urosario/GSIT/2014"]
    user_list = []
    cnx = MongoConnection()
    contents = cnx.find(cnx.query_builder_in("course_id", course_list), "contents")
    print contents


def mysql_process():
    """
    Entry point for our application
    """
    logger.info("Setting up connection to {}@{}".format(settings.DB_DATABASE, settings.DB_HOST))
    cnx = Connection(dict_cursor=True)

    dry_run = settings.GLOBAL_DRY_RUN

    # Your CODE here
    all_ops = []
    for table_name in utils.get_all_tables(cnx):
        try:
            operations = utils.get_operation_for_table(cnx, table_name)
            for operation in operations:
                all_ops.append(operation)

        except OperationError, e:
            logger.error("A Table lacks operations: \033[91m{}\033[00m".format(e.msg))

    # Sort and execute
    logger.info("Executing Operations")
    cnx.execute("SET FOREIGN_KEY_CHECKS=0", dry_run=dry_run)

    all_ops.sort(key=operator.attrgetter('priority'), reverse=True)

    for op in all_ops:
        logger.info("{} => result: {}".format(op, op()))

    if not dry_run:
        cnx._connection.commit()
    cnx.execute("SET FOREIGN_KEY_CHECKS=1", dry_run=dry_run)

    logger.info("Closing connection to DB")
    cnx.close()
