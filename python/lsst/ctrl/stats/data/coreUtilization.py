import sys
import collections
from collections import defaultdict

class DbCoreInfo:
    def __init__(self, info):
        self.executionHost = info[0]
        self.slotName = info[1]
        self.executionStartTime = info[2]

class CoreUtilization:

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
