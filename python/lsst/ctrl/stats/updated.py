from record import Record
class Updated(Record):
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

        pat = "Image size of job updated: (?P<imageSize>[\d]+)"
        
        self.imageSize = int(self.extract(pat,lines[0], "imageSize"))
        
        self.memoryUsageMB = "0"
        if len(lines) == 3:
                pat = "(?P<memoryUsage>[\d]+)"
                self.memoryUsageMB = int(self.extract(pat,lines[1],"memoryUsage"))
        pat = "(?P<residentSetSize>[\d]+)"
        self.residentSetSize = int(self.extract(pat,lines[1],"residentSetSize"))


    def printAll(self):
        print "U",self.lines

    def describe(self):
        s = "%s imageSize=%s" % (self.timestamp, self.imageSize)
        return s
