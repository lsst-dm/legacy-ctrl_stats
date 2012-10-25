class Record(object):
    def __init__(self,lines):
        self.lines = list(lines)

        regex = ur"\(.+?.\)"
        jobNumber = re.findall(regex,lines[0])[0]
        jobNumber = jobNumber.strip("()")
        regex = ur"\d+"
        jobNumber = re.findall(regex,jobNumber)[0]
        print "job number = ",jobNumber

        regex = ur"\d+:\d+:\d+"
        timestamp = re.findall(regex,lines[0])[0]
        print "timestamp: ",timestamp

        regex = r"\<.+?.\>"
        host = re.findall(regex,lines[0])[0]
        host = host.strip("<>")
        print "host: ",host

    def printAll(self):
        print self.lines
