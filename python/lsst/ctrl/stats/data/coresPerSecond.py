import datetime
class CoresPerSecond:

    def __init__(self, dbm):
        self.dbm = dbm

    def calculate(self, entries):
        query = "select UNIX_TIMESTAMP(MIN(executionStartTime)), UNIX_TIMESTAMP(MAX(executionStopTime)) from submissions where UNIX_TIMESTAMP(executionStartTime) > 0 order by executionStartTime;"

        results = self.dbm.execCommandN(query)
        startTime = results[0][0]
        stopTime = results[0][1]

        values = []
        # cycle through the seconds, counting the number of cores being used
        # during each second
        for thisSecond in range(startTime, stopTime+1):
            x = 0
            length = entries.getLength()
            for i in range(length):
                ent = entries.getEntry(i)
                if (thisSecond >= ent.executionStartTime) and (thisSecond <= ent.executionStopTime):
                    x = x + 1
            
            values.append([thisSecond,x])
        return values

