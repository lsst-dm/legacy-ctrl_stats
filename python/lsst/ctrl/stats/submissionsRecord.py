import MySQLdb
from dbRecord import DbRecord

class SubmissionsRecord(DbRecord):
    def __init__(self, rec=None):
        if rec == None:
            self.condorId = None
            self.dagNode = None
            self.submitTime = None
            self.executionHost = None
            self.executionStartTime = "0000-00-00 00:00:00"
            self.executionStopTime = "0000-00-00 00:00:00"
            self.updateImageSize = 0
            self.updateMemoryUsageMb = 0
            self.updateResidentSetSizeKb = 0
            self.userRunRemoteUsage = 0
            self.sysRunRemoteUsage = 0
            self.finalMemoryUsageMb = 0
            self.finalMemoryRequestMb = 0
            self.bytesSent = 0
            self.bytesReceived = 0
            self.terminationTime = None
            self.terminationCode = None
            self.terminationReason = None
        else:
            # this is used instead of copy to initialize values in
            # a superclass from values in object of this type
            self.condorId = rec.condorId
            self.dagNode = rec.dagNode
            self.submitTime = rec.submitTime
            self.executionHost = rec.executionHost
            self.executionStartTime = rec.executionStartTime
            self.executionStopTime = rec.executionStopTime
            self.updateImageSize = rec.updateImageSize
            self.updateMemoryUsageMb = rec.updateMemoryUsageMb
            self.updateResidentSetSizeKb = rec.updateResidentSetSizeKb
            self.userRunRemoteUsage = rec.userRunRemoteUsage
            self.sysRunRemoteUsage = rec.sysRunRemoteUsage
            self.finalMemoryUsageMb = rec.finalMemoryusageMb
            self.finalMemoryRequestMb = rec.finalMemoryRequestMb
            self.bytesSent = rec.bytesSent
            self.bytesReceived = rec.bytesReceived
            self.terminationTime = rec.terminationTime
            self.terminationCode = rec.terminationCode
            self.terminationReason = rec.terminationReason
