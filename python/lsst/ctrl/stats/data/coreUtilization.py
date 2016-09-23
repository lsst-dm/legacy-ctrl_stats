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


class DbCoreInfo(object):
    """
    Class to hold information about the host, slot and the time it started
    """

    def __init__(self, info):
        """
        Constructor
        """
        # the host on which the job was executing
        self.executionHost = info[0]
        # the name of the HTCondor slot
        self.slotName = info[1]
        # start of execution
        self.executionStartTime = info[2]


class CoreUtilization(object):
    """
    Get a listing of all the times at with a core is used.
    """

    def __init__(self, dbm):
        """
        Constructor
        @parameter dbm The database object to query.
        """
        # the database object to query
        self.dbm = dbm

        query = "select executionHost, slotName, min(UNIX_TIMESTAMP(executionStartTime)) from "
        query = query + "submissions where dagNode !='A' and dagNode != 'B'  group by executionHost, "
        query = query + "slotName order by min(UNIX_TIMESTAMP(executionStartTime))"

        results = self.dbm.execCommandN(query)
        # the list of all database records returned
        self.entries = []
        for res in results:
            coreInfo = DbCoreInfo(res)
            self.entries.append(coreInfo)

    def getFirstTime(self):
        """
        retrieve the first execution start time
        """
        return self.entries[0].executionStartTime

    def getLastTime(self):
        """
        retrieve the last execution start time
        """
        return self.entries[-1].executionStartTime

    def coresUtilized(self):
        """
        the maximum of cores that were utilitized
        """
        return len(self.entries)
