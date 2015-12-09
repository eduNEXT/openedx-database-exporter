#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings
import logging
from databases.mysql import Connection

logger = logging.getLogger(__name__)


def main():
    """
    Entry point for our application
    """
    logger.info("Setting up connection to {}@{}".format(settings.DB_DATABASE, settings.DB_HOST))
    cnx = Connection()

    # Your CODE here

    logger.info("Closing connection to DB")
    cnx.close()
