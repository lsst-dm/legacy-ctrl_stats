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
import MySQLdb
class DbRecord(object):

    def printValues(self, obj):
        """uses introspection to print all values for member variables for
        subclasses of this class
        """
        members = [attr for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__")]
        for mem in members:
            value = getattr(self, mem)
            print mem, "=", value

    def getInsertString(self, tableName):
        """uses introspection to create insert string for values for the
        classes which subclass this class.
        """
        members = [attr for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__")]
        cmd = "INSERT INTO %s (" % (tableName)
        first = True
        for mem in members:
            if first:
                add = mem
                first = False
            else:
                add = ", "+mem
            cmd = cmd+add
        cmd = cmd+") VALUES ("
        first = True
        for mem in members:
            value = getattr(self, mem)
            if value is None:
                value = ""
            if first:
                if type(value) == type(str()):
                    add = "'"+MySQLdb.escape_string(value)+"'"
                else:
                    add = str(value)
                first = False
            else:
                if type(value) == type(str()):
                    add = ", '"+MySQLdb.escape_string(value)+"'"
                else:
                    add = ", "+str(value)
            cmd = cmd+add
        cmd = cmd+")"
        return cmd
