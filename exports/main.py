#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings
import logging
from databases.mysql import Connection
from operations.base import OperationError
import operations.utils as utils
import preprocessing

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
    for op in all_ops:
        print op
        print "result: {}".format(op())

    #SET FOREIGN_KEY_CHECKS=0;
    #SET FOREIGN_KEY_CHECKS=1;

    logger.info("Closing connection to DB")
    cnx.close()


users_list = None
courses_list = None


def init_lists(cnx, site, org_list):
    users_list = preprocessing.user_list.get_users_list(cnx, site, org_list)
    courses_list = preprocessing.course_list.get_courses_list(cnx, site, org_list)
