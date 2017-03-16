#
# LSST Data Management System
# Copyright 2008-2012 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#

from lsst.db import utils
from lsst.db.engineFactory import getEngineFromArgs
# from lsst.db.testHelper import readCredentialFile


class DatabaseManager(object):
    """Creates a connection to an sql server

    Parameters
    ----------
    dbHostName: `str`
        a server where the database daemon resides
    portNumber: `int`
        the port number the database daemon is listening on
    user: `str`
        the user name to connect as
    passwd: `str`
        the users's password
    """

    def __init__(self, dbHostName, portNumber, user, passwd):
        self.conn = getEngineFromArgs(username=user, password=passwd,
                                      host=dbHostName,
                                      port=portNumber).connect()

    def loadSql(self, filePath, database):
        """Load an SQL file into a database
        @param filePath: the SQL file to load
        @param database: the database to use
        """
        utils.loadSqlScript(self.conn, filePath, database)

    def execCommand0(self, cmd, *args):
        """Execute a command with no results
        @param cmd SQL command to execute
        """
        self.conn.execute(cmd, *args)

    def execCommand1(self, cmd):
        """Execute a command with one result
        @param cmd SQL command to execute
        @return single result
        """
        results = self.conn.execute(cmd)
        val = results.fetchone()
        items = val.items()
        return items[0][1]

    def execCommandN(self, cmd):
        """Execute a command with N results
        @param cmd SQL command to execute
        @return results
        """
        result = self.conn.execute(cmd)
        values = result.fetchall()
        return values

    def dbExists(self, dbName):
        """Check for database existence
        @return True if database exists, False otherwise
        """
        return utils.dbExists(self.conn, dbName)

    def createDb(self, dbName):
        """Create a database
        @param dbName name of database to create
        """
        utils.createDb(self.conn, dbName)

    def close(self):
        """Close connection to server
        """
        self.conn.close()
        self.conn = None
