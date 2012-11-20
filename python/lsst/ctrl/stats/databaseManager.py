#!/usr/bin/env python

from lsst.cat.MySQLBase import MySQLBase
import MySQLdb

class DatabaseManager(MySQLBase):
    def __init__(self, dbHostName, portNumber, user, password):
        MySQLBase.__init__(self, dbHostName, portNumber)
        self.user = user
        self.password = password

        self.connect(user,password)

    def execute(self, ins):
        self.execCommand0(ins)

    def loadSql(self, filePath, database):
        self.loadSqlScript(filePath, self.user, self.password, database)
