import re

class Record(object):
    def __init__(self,lines):
        self.lines = list(lines)

        pat = r"(?P<num>\d+) " + \
            r"\((?P<jobNum>.+?.)\) " + \
            r"(?P<date>\d+\/\d+) " + \
            r"(?P<timestamp>\d+:\d+:\d+) "

        info = re.search(pat,lines[0])
        if info is not None:
            values = info.groupdict()
            print values
        self.num = values["num"]
        self.jobNum = values["jobNum"]
        self.date = values["date"]
        self.timestamp = values["timestamp"]

    def printAll(self):
        print "num ",self.num
        print "jobNum ",self.jobNum
        print "date ",self.date
        print "timestamp ",self.timestamp


    def extractValues(self,pat,line):
        values = re.search(pat,line).groupdict()
        return values

    def extract(self,pat,line,tag):
        values = re.search(pat,line).groupdict()
        val = values[tag]
        return val

    def extractPair(self, pat, line, tag1, tag2):
        print line
        values = self.extractValues(pat, line)
        print "values = ",values
        print "tag1",tag1
        print "tag2",tag2
        val1 = values[tag1]
        val2 = values[tag2]
        return val1, val2

    def extractUsrSysTimes(self, line):
        pat = r"Usr \d+ " + \
                r"(?P<usr>\d+:\d+:\d+), "  + \
                r"Sys \d+ " + \
                r"(?P<sys>\d+:\d+:\d+) "
        return self.extractPair(pat, line, "usr", "sys")
