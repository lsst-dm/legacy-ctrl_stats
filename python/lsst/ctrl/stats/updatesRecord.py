import MySQLdb
from dbRecord import DbRecord

class UpdatesRecord(DbRecord):
    def __init__(self, rec=None):
        if rec == None:
            self.condorId = None
            self.dagNode = None
            self.executionHost = None
            self.timestamp = "0000-00-00 00:00:00"
            self.imageSize = 0
            self.memoryUsageMb = 0
            self.residentSetSizeKb = 0
