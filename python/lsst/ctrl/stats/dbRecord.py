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

    def getInsertQuery(self, tableName):
        """Create insert string for values for member variables of the class.
        @param tableName: the table name in which this record will be put
        """
        members = [attr for attr in dir(self) if not callable(
            getattr(self, attr)) and not attr.startswith("__")]

        values = [getattr(self, mem) for mem in members]
        values = ["" if value is None else value for value in values]

        # string like "%s,%s,%s,%s,..."
        valuePlaceholders = ','.join(['%s']*len(members))
        columns = ",".join(members)
        cmd = "INSERT INTO {} ({}) VALUES ({})".format(tableName, columns,
                                                       valuePlaceholders)
        # return non-interpolated query and value list
        return cmd, values
