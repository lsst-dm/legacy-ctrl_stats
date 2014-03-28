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

from lsst.cat.MySQLBase import MySQLBase

class DatabaseManager(MySQLBase):
    """Convenience class the MySQLBase class with which we hold the
    the username and password.  We do this so we can pass this object
    around and not have to pass the user name and password all over 
    the place.  Note: It was pointed out that this functionality may be
    better placed in MySQLBase itself, and if that happens this code
    should be removed and that new code should be used instead.
    """
    def __init__(self, dbHostName, portNumber, user, password):
        """Creates a connection to a MySQL server
        @param dbHostName: a server where the MySQL daemon resides
        @param portNumber: the port number the MySQL daemon is listening on
        @param user: the user name to connect as
        @param password: the users's password
        """
        MySQLBase.__init__(self, dbHostName, portNumber)
        ## user
        self.user = user
        ## password
        self.password = password

        self.connect(user,password)

    def loadSql(self, filePath, database):
        """Load an SQL file into a database
        @param filePath: the SQL file to load
        @param database: the database to use
        """
        self.loadSqlScript(filePath, self.user, self.password, database)
