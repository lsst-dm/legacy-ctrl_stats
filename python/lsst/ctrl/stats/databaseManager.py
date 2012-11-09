#!/usr/bin/env python

from lsst.cat.MySQLBase import MySQLBase
import MySQLdb

class DatabaseManager(MySQLBase):
    def __init__(self, dbHostName, portNumber):
        MySQLBase.__init__(self, dbHostName, portNumber)


    def execute(self, ins):
        self.execCommand0(ins)

