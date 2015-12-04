#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb


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

    def __init__(self, host='localhost', user='root', passwd='', db=''):
        self._host = host
        self._user = user
        self._passwd = passwd
        self._db = db

        self._open(dict_cursor=True)

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

    def execute(self, query, args=None):
        self._session.execute(query, args)
        return self._session.fetchall()