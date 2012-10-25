class Record(object):
    def __init__(self,lines):
        self.lines = list(lines)

    def printAll(self):
        print self.lines
