#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings
from databases.mysql import Connection


def main():
    """
    Entry point for our application
    """
    cnx = Connection(
        db="mysql",
    )

    for row in cnx.execute("""SELECT * FROM user"""):
        print row["Host"]

    cnx.close()
