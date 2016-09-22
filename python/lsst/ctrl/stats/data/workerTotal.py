from builtins import object
#
# LSST Data Management System
# Copyright 2008-2013 LSST Corporation.
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


class WorkerTotal(object):
    """
    Count the total number of workers. does not include the preJob or postJob
    """

    def __init__(self, dbm):
        """
        Constructor
        """
        # database object to use in query
        self.dbm = dbm

    def getTotal(self, tableName):
        """
        return the total number of workers, not including prejob and postjob
        @return total number of workers
        """
        query = "select  count(dagNode) from %s where dagNode != 'A' and dagNode != 'B'" % tableName

        results = self.dbm.execCommand1(query)

        return results
