import re
from record import Record
class Evicted(Record):
    """
    Job evicted from machine
    A job was removed from a machine before it was finished.
    """
    # event number: 004
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

        self.reason = lines[1].strip()



        pat = r"\((?P<term>\d+)\) Job was not checkpointed."

        self.term = self.extract(pat, lines[1], "term")

        self.userRunRemoteUsage, self.sysRunRemoteUsage = self.extractUsrSysTimes(lines[2])

        self.userRunLocalUsage,  self.sysRunLocalUsage  = self.extractUsrSysTimes(lines[3])


        pat = r"(?P<bytes>\d+) "
        self.runBytesSent = int(self.extract(pat,lines[4], "bytes"))
        self.runBytesReceived = int(self.extract(pat,lines[5], "bytes"))


        pat = r":\s+(?P<usage>\d+)\s+(?P<request>\d+)$"

        self.diskUsage = "-1"
        line = lines[8].strip()
        values = re.search(pat,line)
        if values is not None:
            self.diskUsage, self.diskRequest = self.extractPair(pat,line,"usage","request")
        else:
            pat = r":\s+(?P<request>\d+)$"
            self.diskRequest = self.extract(pat,line,"request")

        self.memoryUsage = "-1"
        line = lines[9].strip()
        values = re.search(pat,line)
        if values is not None:
            self.memoryUsage, self.memoryRequest = self.extractPair(pat,line,"usage","request")
        else:
            pat = r":\s+(?P<request>\d+)$"
            self.memoryRequest = self.extract(pat,line,"request")

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

    def describe(self):
        s = "%s reason=%s" % (self.timestamp, self.reason)
        return s
