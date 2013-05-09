import datetime
from lsst.ctrl.stats.data.coresPer import CoresPer
class CoresPerSecond(CoresPer):

    def __init__(self, dbm, entries):
        self.dbm = dbm

        query = "select UNIX_TIMESTAMP(MIN(executionStartTime)), UNIX_TIMESTAMP(MAX(executionStopTime)) from submissions where UNIX_TIMESTAMP(executionStartTime) > 0 and dagNode != 'A' and dagNode != 'B' order by executionStartTime;"

        results = self.dbm.execCommandN(query)
        startTime = results[0][0]
        stopTime = results[0][1]

        self.values = []
        # cycle through the seconds, counting the number of cores being used
        # during each second
        for thisSecond in range(startTime, stopTime+1):
            x = 0
            length = entries.getLength()
            for i in range(length):
                ent = entries.getEntry(i)
                if ent.dagNode == 'A':
                    continue
                if ent.dagNode == 'B':
                    continue
                if (thisSecond >= ent.executionStartTime) and (thisSecond <= ent.executionStopTime):
                    x = x + 1
            
            self.values.append([thisSecond,x])

        self.maximumCores, self.timeFirstUsed, self.timeLastUsed = calculateMax()
