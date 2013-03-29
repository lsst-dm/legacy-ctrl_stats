import collections
from collections import defaultdict

class DbStartInfo:
    def __init__(self, info):
        self.dagNode = info[0]
        self.executionHost = info[1]
        self.slotName = info[2]
        self.executionStartTime = info[3]
        self.terminationTime = info[4]
        self.timeToNext = -1

class NewJobStart:

    def __init__(self, dbm):
        self.dbm = dbm

        query = "select dagNode, executionHost, slotName, UNIX_TIMESTAMP(executionStartTime), UNIX_TIMESTAMP(terminationTime) from submissions where dagNode != 'A' and dagNode !='B' order by executionHost, slotName, executionStartTime;"

        results = self.dbm.execCommandN(query)
        self.entries = []
        for res in results:
            startInfo = DbStartInfo(res)
            self.entries.append(startInfo)

    def calculate(self):
        mylist = []
        for ent in self.entries:
            mylist.append((ent.executionHost+"/"+ent.slotName,[ent.executionStartTime,ent.terminationTime]))
        d = defaultdict(list)
        for k,v in mylist:
            d[k].append(v)

        totals = {}
        for item in d:
            timeList = d[item]
            length = len(timeList)
            for i in range(length-1):
                timeToNext = timeList[i+1][0] - timeList[i][1]
                if timeToNext not in totals:
                    totals[timeToNext] = 1
                else:
                    totals[timeToNext] = totals[timeToNext] + 1
        od = collections.OrderedDict(sorted(totals.items()))
        return od
                
        return od
            

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
                
