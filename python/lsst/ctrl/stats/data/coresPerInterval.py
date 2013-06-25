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
import datetime
from lsst.ctrl.stats.data.coresPer import CoresPer
#
# count the number of cores that are active during a specific interval
#
class CoresPerInterval(CoresPer):

    def __init__(self, dbm, entries, interval):
        self.dbm = dbm

        query = "select UNIX_TIMESTAMP(MIN(executionStartTime)), UNIX_TIMESTAMP(MAX(executionStopTime)) from submissions where UNIX_TIMESTAMP(executionStartTime) > 0 and dagNode != 'A' and dagNode != 'B' order by executionStartTime;"

        results = self.dbm.execCommandN(query)
        startTime = results[0][0]
        stopTime = results[0][1]

        self.values = []
        # cycle through the seconds, counting the number of cores being used
        # during each second
        last = startTime
        if (startTime+interval > stopTime):
            next = stopTime
        else:
            next = startTime+interval
        stepInterval = 0
        while True:
            x = 0
            length = entries.getLength()
            intervalRangeSet = set(range(last,next+1))

            for i in range(length):
                ent = entries.getEntry(i)
                entryRangeSet = set(range(ent.executionStartTime, ent.executionStopTime+1))
                if (len(intervalRangeSet&entryRangeSet) > 0):
                    x = x + 1
            
            self.values.append([last,x])
            stepInterval = stepInterval+1

            if next >= stopTime:
                return
            last = next
            if (next+interval) > stopTime:
                next = stopTime
            else:
                next = next+interval
            
        self.maximumCores, self.timeFirstUsed, self.timeLastUsed = calculateMax()
