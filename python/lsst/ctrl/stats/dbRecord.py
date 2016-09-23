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
from __future__ import print_function
from builtins import str
from builtins import bytes
from builtins import object
import MySQLdb


class DbRecord(object):
    """Base class for database record objects.  This object uses introspection
    to discover the names of member variables used in subclasses to create
    it's output.  This allows the additions/deletions of fields in a
    subclassed object without having to make changes to methods.

    The names of the fields in those objects are expected to match those
    of the database table in which they are being written.
    """

    def printValues(self):
        """Print all values for member variables for subclasses of this class
        """
        members = [attr for attr in dir(self) if not callable(
            getattr(self, attr)) and not attr.startswith("__")]
        for mem in members:
            value = getattr(self, mem)
            print(mem, "=", value)

    def getInsertString(self, tableName):
        """Create insert string for values for the member variables of the class.
        @param tableName: the table name in which this record will be put
        """
        members = [attr for attr in dir(self) if not callable(
            getattr(self, attr)) and not attr.startswith("__")]

        # columns names
        columns = ",".join(members)

        # MySQL escaped strings and values
        valueList = []
        for mem in members:
            value = getattr(self, mem)
            if value is None:
                value = ""
            if isinstance(value, (bytes, str)):
                value = MySQLdb.escape_string(value)
                if isinstance(value, bytes):
                    value = "'" + value.decode() + "'"
                else:
                    value = "'"+value+"'"
            else:
                value = str(value)
            valueList.append(value)
        values = ",".join(valueList)

        cmd = "INSERT INTO %s (%s) VALUES (%s)" % (tableName, columns, values)

        return cmd
