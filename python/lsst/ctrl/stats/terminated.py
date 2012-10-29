import re
from record import Record
class Terminated(Record):
    def __init__(self, lines):
        Record.__init__(self,lines)

        pat = r"\((?P<term>\d+)\) Normal termination \(return value (?P<returnValue>\d+)\)"

        self.term, self.returnValue = self.extractPair(pat, lines[1], "term", "returnValue")

        self.userRunRemoteUsage, self.sysRunRemoteUsage = self.extractUsrSysTimes(lines[2])

        self.userRunLocalUsage,  self.sysRunLocalUsage  = self.extractUsrSysTimes(lines[3])

        self.userTotalRemoteUsage, self.sysTotalRemoteUsage = self.extractUsrSysTimes(lines[4])

        self.userTotalLocalUsage,  self.sysTotalLocalUsage  = self.extractUsrSysTimes(lines[5])

        pat = r"(?P<bytes>\d+) "
        self.runBytesSent = self.extract(pat,lines[6], "bytes")
        self.runBytesReceived = self.extract(pat,lines[7], "bytes")
        self.totalBytesSent = self.extract(pat,lines[8], "bytes")
        self.totalBytesReceived = self.extract(pat,lines[9], "bytes")


    def printAll(self):
        Record.printAll(self)
        print "term = ",self.term
        print "returnValue = ",self.returnValue
        print "userRunRemoteUsage = ", self.userRunRemoteUsage
        print "sysRunRemoteUsage = ", self.sysRunRemoteUsage
        print "userRunLocaleUsage = ", self.userRunLocalUsage
        print "sysRunLocaleUsage = ", self.sysRunLocalUsage

        print "userTotalRemoteUsage = ", self.userTotalRemoteUsage
        print "sysTotalRemoteUsage = ", self.sysTotalRemoteUsage
        print "userTotalLocaleUsage = ", self.userTotalLocalUsage
        print "sysTotalLocaleUsage = ", self.sysTotalLocalUsage

        print "runBytesSent ",self.runBytesSent
        print "runBytesReceived ",self.runBytesReceived
        print "totalBytesSent ",self.totalBytesSent
        print "totalBytesReceived ",self.totalBytesReceived
