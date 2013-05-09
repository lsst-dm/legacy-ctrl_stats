import datetime
from lsst.ctrl.stats.data.coresPer import CoresPer
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
                if ent.dagNode == 'A':
                    continue
                if ent.dagNode == 'B':
                    continue
                entryRangeSet = set(range(ent.executionStartTime, ent.executionStopTime+1))
                if (len(intervalRangeSet&entryRangeSet) > 0):
                    x = x + 1
            
            self.values.append([last,x])
            stepInterval = stepInterval+1

            if (next >= stopTime):
                return
            last = next
            if (next+interval > stopTime):
                next = stopTime
            else:
                next = next+interval
            
        self.maximumCores, self.timeFirstUsed, self.timeLastUsed = calculateMax()
