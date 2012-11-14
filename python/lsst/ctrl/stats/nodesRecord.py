import MySQLdb
from dbRecord import DbRecord

class NodesRecord(DbRecord):
    def __init__(self):
        self.condorId = None
        self.dagNode = None
        self.submitTime = None
        self.executionHost = None
        self.executionStartTime = "0000-00-00 00:00:00"
        self.executionStopTime = "0000-00-00 00:00:00"
        self.updateImageSize = 0
        self.updateMemoryUsageMB = 0
        self.updateResidentSetSize = 0
        self.userRunRemoteUsage = 0
        self.sysRunRemoteUsage = 0
        self.finalMemoryUsageMB = 0
        self.finalMemoryRequestMB = 0
        self.bytesSent = 0
        self.bytesReceived = 0
        self.terminationTime = None
        self.terminationCode = None
        self.terminationReason = None
