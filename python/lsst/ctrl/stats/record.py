import re
import sys

class Record(object):
    def __init__(self, year, lines):
        self.lines = list(lines)

        pat = r"(?P<event>\d+) " + \
            r"\((?P<jobNum>.+?.)\) " + \
            r"(?P<month>\d+)\/(?P<day>\d+) " + \
            r"(?P<timestamp>\d+:\d+:\d+) "

        info = re.search(pat,lines[0])
        values = {}
        if info is not None:
            values = info.groupdict()
            self.event = values["event"]
            self.jobNum = values["jobNum"]
            self.timestamp = str(year)+"-"+values["month"]+"-"+values["day"]+" "+values["timestamp"]
        else:
            print "error parsing record:"
            print lines[0]
            sys.exit(10)

    def printAll(self):
        print "event ",self.event
        print "jobNum ",self.jobNum
        print "timestamp ",self.timestamp


    def extractValues(self,pat,line):
        try:
            values = re.search(pat,line).groupdict()
            return values
        except AttributeError:
            print "exiting"
            sys.exit(100)

    def extract(self,pat,line,tag):
        values = re.search(pat,line).groupdict()
        val = values[tag]
        return val

    def extractPair(self, pat, line, tag1, tag2):
        values = self.extractValues(pat, line)
        val1 = values[tag1]
        val2 = values[tag2]
        return val1, val2

    def extractUsrSysTimes(self, line):
        pat = r"Usr \d+ " + \
                r"(?P<usr>\d+:\d+:\d+), "  + \
                r"Sys \d+ " + \
                r"(?P<sys>\d+:\d+:\d+) "
        return self.extractPair(pat, line, "usr", "sys")

    def describe(self):
        s = "%s %s" % (self.jobNum, self.timestamp)
        return s
