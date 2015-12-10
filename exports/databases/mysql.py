#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from .. import settings

import logging

logger = logging.getLogger(__name__)


class Connection(object):
    """
        Python Class for connecting  with MySQL
    """
    _host = None
    _user = None
    _passwd = None
    _db = None

    _session = None
    _connection = None

    def __init__(self, host=settings.DB_HOST, user=settings.DB_USER, passwd=settings.DB_PASSWD, db=settings.DB_DATABASE, dict_cursor=False):
        self._host = host
        self._user = user
        self._passwd = passwd
        self._db = db

        self._open(dict_cursor=dict_cursor)

    def _open(self, *args, **kwargs):
        """ Create the connection and the cursor """
        self._connection = MySQLdb.connect(
            host=self._host,
            user=self._user,
            passwd=self._passwd,
            db=self._db,
        )

        if kwargs.get('dict_cursor', False):
            self._session = self._connection.cursor(MySQLdb.cursors.DictCursor)
        else:
            self._session = self._connection.cursor()

    def close(self):
        """ Close the connection. Probably should be called during __del__ """
        self._session.close()
        self._connection.close()

    def execute(self, query, args=None, dry_run=False):
        if dry_run:
            logging.debug("Executing: {} with args:{}".format(query, unicode(args)[:100]))
            return

        try:
            self._session.execute(query, args)
        except Exception as e:
            print "Error on query: "+self._session._last_executed
            raise e

        return self._session.fetchall()
