import MySQLdb
from dbRecord import DbRecord

class ExecutionsRecord(DbRecord):
    def __init__(self, rec=None):
        if rec == None:
            self.condorId = None
            self.dagNode = None
            self.executionHost = None
            self.imageSize = 0
            self.memoryUsageMb = 0
            self.residentSetSizeKb = 0
