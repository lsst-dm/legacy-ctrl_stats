import sys
class ExecutionsPerSlot:

    def __init__(self, dbm):
        self.dbm = dbm
        query = "select concat(executionHost, '/', slotName) as slot, count(*) as timesUsed from submissions group by executionHost, slotName;"

        self.results = self.dbm.execCommandN(query)

    def average(self):
        avg = 0
        for res in self.results:
            avg = avg + res[1]
        return int(avg/len(self.results)+0.5)
            

    def min(self):
        m = sys.maxint
        for res in self.results:
            if m > res[1]:
                m = res[1]
        return m

    def max(self):
        m = -sys.maxint -1
        for res in self.results:
            if res[1] > m:
                m = res[1]
        return m
