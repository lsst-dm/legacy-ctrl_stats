class DbRecord(object):
    def __init__(self):
        self.condorId = None
        self.dagNode = None
        self.submitTime = None
        self.executionHost = None
        self.executionStartTime = None
        self.executionStopTime = None
        self.userRunRemoteUsage = None
        self.sysRunRemoteUsage = None
        self.userRunLocalUsage = None
        self.sysRunLocalUsage = None
        self.bytesSent = None
        self.bytesReceived = None
        self.evicted = None
        self.terminationTime = None
        self.terminationCode = None
        self.terminationReason = None
