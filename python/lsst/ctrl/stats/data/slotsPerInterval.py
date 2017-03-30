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
from builtins import range
from lsst.ctrl.stats.data.slotsPer import SlotsPer


class SlotsPerInterval(SlotsPer):
    """Count the number of slots that are active during a specific interval

    Parameters
    ----------
    dbm: `DatabaseManager`
        the database object to query
    entries: dbEntry list
        the set of entries to compare
    interval: `int`
        seconds
    """

    def __init__(self, dbm, entries, interval):
        # the database object to query
        self.dbm = dbm

        query = "select UNIX_TIMESTAMP(MIN(executionStartTime)), \
UNIX_TIMESTAMP(MAX(executionStopTime)) from submissions where \
UNIX_TIMESTAMP(executionStartTime) > 0 and dagNode != 'A' and \
dagNode != 'B' and slotName != '' order by executionStartTime;"

        results = self.dbm.execCommandN(query)
        startTime = results[0][0]
        stopTime = results[0][1]

        # computed values
        self.values = []
        # cycle through the seconds, counting the number of slots being used
        # during each second
        last = startTime
        if (startTime+interval > stopTime):
            nextTime = stopTime
        else:
            nextTime = startTime+interval
        stepInterval = 0
        while True:
            x = 0
            length = entries.getLength()
            intervalRangeSet = set(range(last, nextTime+1))

            for i in range(length):
                ent = entries.getEntry(i)
                entryRangeSet = set(range(ent.executionStartTime,
                                    ent.executionStopTime+1))
                if (len(intervalRangeSet & entryRangeSet) > 0):
                    x = x + 1

            self.values.append([last, x])
            stepInterval = stepInterval+1

            if nextTime >= stopTime:
                return
            last = nextTime
            if (nextTime+interval) > stopTime:
                nextTime = stopTime
            else:
                nextTime = nextTime+interval

        maximumSlots, timeFirstUsed, timeLastUsed = self.calculateMax()
        # the maximum number of slots used
        self.maximumSlots = maximumSlots
        # the first time at which a slot was used for this job
        self.timeFirstUsed = timeFirstUsed
        # the last time at which a slot was used for this job
        self.timeLastUsed = timeLastUsed
