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
import sys
import collections
from collections import defaultdict

class DbCoreInfo:
    """
    class to hold information about the host, slot and the time it started
    """
    def __init__(self, info):
        self.executionHost = info[0]
        self.slotName = info[1]
        self.executionStartTime = info[2]

class CoreUtilization:
    """
    get a listing of all the times at with a core is used.
    """

    def __init__(self, dbm):
        self.dbm = dbm

        query = "select executionHost, slotName, min(UNIX_TIMESTAMP(executionStartTime)) from submissions where dagNode !='A' and dagNode != 'B'  group by executionHost, slotName order by min(UNIX_TIMESTAMP(executionStartTime))"

        results = self.dbm.execCommandN(query)
        self.entries = []
        for res in results:
            coreInfo = DbCoreInfo(res)
            self.entries.append(coreInfo)

    def getFirstTime(self):
        return self.entries[0].executionStartTime
                
    def getLastTime(self):
        return self.entries[-1].executionStartTime

    def coresUtilized(self):
        return len(self.entries)
