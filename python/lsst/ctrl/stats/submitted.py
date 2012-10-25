import re
from record import Record

class Submitted(Record):
    def __init__(self, lines):
        Record.__init__(self,lines)

        regex = ur"\(.+?.\)"
        jobNumber = re.findall(regex,lines[0])[0]
        jobNumber = jobNumber.strip("()")
        regex = ur"\d+"
        jobNumber = re.findall(regex,jobNumber)[0]
        print "job number = ",jobNumber

        regex = ur"\d+:\d+:\d+"
        timestamp = re.findall(regex,lines[0])[0]
        print "time: ",timestamp

        regex = r"\<.+?.\>"
        host = re.findall(regex,lines[0])[0]
        host = host.strip("<>")
        print "host: ",host

        regex = ur"DAG Node: (.+?)$"
        worker = re.findall(regex,lines[1])[0]
        print "worker = ",worker

    def printAll(self):
        print "S",self.lines
