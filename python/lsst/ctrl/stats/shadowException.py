import re
from record import Record
class ShadowException(Record):
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

        
        print "lines[1] = ",lines[1]
        pat = r"Error from (?P<slot>[\w]+@[\d]+@[\w\-.]+): (?P<reason>.+?)($)"
        self.slot = None
        self.reason = None
        self.runBytesSent = None
        self.runBytesReceived = None
        if re.search(pat,lines[1]) is not None:
            values = self.extractValues(pat,lines[1])
            self.slot = values["slot"]
            self.reason = values["reason"]
        else:
            self.reason = lines[1]
            pat = r"(?P<bytes>[\d]+)"
            self.runBytesSent = self.extract(pat,lines[2],"bytes")
            self.runBytesReceived = self.extract(pat,lines[3],"bytes")

    def printAll(self):
        Record.printAll(self)
        print "slot = ",self.slot
        print "reason = ",self.reason
        print "runBytesSent = ",self.runBytesSent
        print "runBytesReceived = ",self.runBytesReceived 
