import re
from record import Record
class Evicted(Record):
    def __init__(self, lines):
        Record.__init__(self,lines)

        self.reason = lines[1]



        pat = r"\((?P<term>\d+)\) Job was not checkpointed."

        self.term = self.extract(pat, lines[1], "term")

        self.userRunRemoteUsage, self.sysRunRemoteUsage = self.extractUsrSysTimes(lines[2])

        self.userRunLocalUsage,  self.sysRunLocalUsage  = self.extractUsrSysTimes(lines[3])

        pat = r"(?P<bytes>\d+) "
        self.runBytesSent = self.extract(pat,lines[4], "bytes")
        self.runBytesReceived = self.extract(pat,lines[5], "bytes")


        # TODO: figure out how to deal with the rest of this:
        # 
        # Partitionable Resources :    Usage  Request
        #    Cpus                 :                 1
        #    Disk (KB)            :       10       10
        #    Memory (MB)          :               674

    def printAll(self):
        Record.printAll(self)
        print "term = ",self.term
        print "reason = ",self.reason

        print "userRunRemoteUsage = ", self.userRunRemoteUsage
        print "sysRunRemoteUsage = ", self.sysRunRemoteUsage
        print "userRunLocaleUsage = ", self.userRunLocalUsage
        print "sysRunLocaleUsage = ", self.sysRunLocalUsage

        print "runBytesSent ",self.runBytesSent
        print "runBytesReceived ",self.runBytesReceived


