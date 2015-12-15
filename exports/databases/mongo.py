#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from .. import settings

import logging

logger = logging.getLogger(__name__)


class Connection(object):
    """
        Python Class for connecting  with Mongo
    """
    _host = None
    _port = None
    _db = None

    _client = None

    def __init__(self, host=settings.MONGO_HOST, port=settings.MONGO_PORT, db=settings.MONGO_DATABASE):
        self._host = host
        self._db = db
        self._port = port
        self._client = MongoClient("mongodb://{}:{}".format("192.168.0.185", "27017"))

    def find(self, query, collection, dataset=None, dry_run=False):
        if dataset is None:
            dataset = self._db
        if dry_run:
            logging.debug("{}.{}.find({})".format(dataset, collection, query))
            return
        db = self._client[dataset]
        cursor = db[collection].find(query).limit(10)
        return list(cursor)

    def remove(self, query, collection, dataset=None, dry_run=False):
        if dataset is None:
            dataset = self._db
        if dry_run:
            logging.debug("{}.{}.remove({})".format(dataset, collection, query))
            return
        db = self._client[dataset]
        cursor = db[collection].delete_many(query)
        return cursor.raw_result

    def query_builder_in(self, field_key, field_list, negate=True):
        if negate:
            query = {field_key: {"$not": {"$in": field_list}}}
        else:
            query = {field_key: {"$in": field_list}}
        return query
