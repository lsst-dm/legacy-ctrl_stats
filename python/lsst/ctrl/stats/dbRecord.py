class DbRecord(object):
    def __init__(self, records):
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

        fExecuting = False
        imageSize = 0
        for rec in records:
            if rec.event == CondorEvents.SubmitEvent:
                self.condorId = rec.condorId
                self.dagNode = rec.dagNode
                self.submitTime = rec.timestamp
            elif rec.event == CondorEvent.ExecutingEvent:
                if fExecuting is False:
                    self.executionHost = rec.hostAddr
                    self.executionStartTime = rec.timestamp
                else:
                    # TODO: raise an exception here
                    print "This shouldn't happend"
                fExecuting = True
            elif rec.event == CondorEvents.UpdatedEvent:
               imageSize = imageSize + int(rec.imageSize) 
            elif rec.event == CondorEvents.Terminated:
                self.executionStopTime = rec.timestamp
                self.userRunRemoteUsage = rec.userRunRemoteUsage
                self.sysRunRemoteUsage = rec.sysRunRemoteUsage
                self.userRunLocalUsage = rec.userRunLocalUsage
                self.sysRunLocalUsage = rec.sysRunLocalUsage
                self.bytesSent = rec.runBytesSent
                self.bytesReceived = rec.runBytesReceived
                self.terminationTime = rec.timestamp
                self.terminationCode = rec.event
                self.terminationReason = "Terminated normally"
            elif rec.event == CondorEvents.EvictedEvent:
                fEvicted = True
                self.executionStopTime = rec.timestamp
                self.terminationReason = rec.reason
                self.userRunRemoteUsage = rec.userRunRemoteUsage
                self.sysRunRemoteUsage = rec.sysRunRemoteUsage
                self.runBytesSent = rec.runBytesSent 
                self.runBytesReceived = rec.runBytesReceived
            elif rec.event == CondorEvents.AbortedEvent:
                if self.terminationReason == None:
                    self.terminationReason = rec.reason
            elif rec.event == ShadowExeceptionEvent:
                self.executionStopTime = rec.timestamp
                self.terminationReason = rec.reason
