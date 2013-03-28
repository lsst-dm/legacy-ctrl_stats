import collections
class DbStartInfo:
    def __init__(self, info):
        self.dagNode = info[0]
        self.hostAndSlot = info[1]
        self.executionStartTime = info[2]
        self.executionStopTime = info[3]
        self.secondsTilNext = info[4]

class NewJobStart:

    def __init__(self, dbm):
        self.dbm = dbm

        query = "select t1.dagNode, concat(t1.executionHost, '/', t1.slotName),  UNIX_TIMESTAMP(t1.executionStartTime), UNIX_TIMESTAMP(t1.executionStopTime), UNIX_TIMESTAMP( ( select min(t2.executionStartTime) as started from totals as t2 where t2.executionStartTime > t1.terminationTime and t1.executionHost = t2.executionHost and t1.slotName = t2.slotName)) - UNIX_TIMESTAMP(t1.executionStopTime) as inSeconds from totals as t1;"

        results = self.dbm.execCommandN(query)
        self.entries = []
        for res in results:
            startInfo = DbStartInfo(res)
            self.entries.append(startInfo)

    def consolidate(self):
        totals = {}
        for ent in self.entries:
            if ent.secondsTilNext is None:
                continue
            if ent.secondsTilNext not in totals:
                totals[ent.secondsTilNext] = 1
            else:
                totals[ent.secondsTilNext] = totals[ent.secondsTilNext] + 1
        od = collections.OrderedDict(sorted(totals.items()))
        return od
                
