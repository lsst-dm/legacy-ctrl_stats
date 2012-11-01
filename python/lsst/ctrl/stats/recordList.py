from collections import OrderedDict
import itertools
class RecordList(object):
    def __init__(self):
        self.records = OrderedDict()

    def append(self, rec):
        jobNum = rec.jobNum
        if self.records.has_key(jobNum):
            list = self.records[jobNum]
            list.append(rec)
        else:
            list = []
            list.append(rec)
            self.records[jobNum] = list

    def printAll(self):
        for i in self.records:
            print i 
            for rec in self.records[i]:
                print rec.printAll()

    def printGroups(self):
        for i in self.records:
            
           for rec in self.records[i]:
                print i, rec.__class__.__name__,rec.date,rec.timestamp
           print
