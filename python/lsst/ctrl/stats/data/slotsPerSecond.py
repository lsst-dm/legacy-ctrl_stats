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


class SlotsPerSecond(SlotsPer):
    """calculate the number of slots that are being used each second of the
    execution time span

    dbm: `DatabaseManager`
        the DatabaseManager to query with
    entries: list of DbEntry
        entries to compare
    """

    def __init__(self, dbm, entries):
        # the database object to query
        self.dbm = dbm

        query = "select UNIX_TIMESTAMP(MIN(executionStartTime)), \
UNIX_TIMESTAMP(MAX(executionStopTime)) from submissions where \
UNIX_TIMESTAMP(executionStartTime) > 0 and dagNode != 'A' \
and dagNode != 'B' and slotName != '' order by executionStartTime;"

        results = self.dbm.execCommandN(query)
        startTime = results[0][0]
        stopTime = results[0][1]

        # the intervals between entries
        self.values = []
        # cycle through the seconds, counting the number of slots being used
        # during each second
        for thisSecond in range(startTime, stopTime+1):
            x = 0
            length = entries.getLength()
            for i in range(length):
                ent = entries.getEntry(i)
                if (thisSecond >= ent.executionStartTime) and \
                   (thisSecond <= ent.executionStopTime):
                        x = x + 1

            self.values.append([thisSecond, x])

        maximumSlots, timeFirstUsed, timeLastUsed = self.calculateMax()
        # the maximum number of slots use
        self.maximumSlots = maximumSlots
        # the first time at which a slot was used for this job
        self.timeFirstUsed = timeFirstUsed
        # the last time at which a slot was used for this job
        self.timeLastUsed = timeLastUsed
