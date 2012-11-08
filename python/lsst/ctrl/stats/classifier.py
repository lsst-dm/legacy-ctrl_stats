from condorEvents import CondorEvents
from dbRecord import DbRecord

class Classifier(object):
    def classify(self, records):
        entries = []

        entry = DbRecord()

        fExecuting = False
        imageSize = 0
        for rec in records:
            if rec.event == CondorEvents.SubmittedEvent:
                entry.condorId = rec.condorId
                self.dagNode = rec.dagNode
                entry.submitTime = rec.timestamp
            elif rec.event == CondorEvents.ExecutingEvent:
                if fExecuting is False:
                    entry.executionHost = rec.executingHostAddr
                    entry.executionStartTime = rec.timestamp
                #else:
                #    # TODO: raise an exception here
                #    print "This shouldn't happend"
                fExecuting = True
            elif rec.event == CondorEvents.UpdatedEvent:
               imageSize = imageSize + int(rec.imageSize) 
            elif rec.event == CondorEvents.TerminatedEvent:
                entry.executionStopTime = rec.timestamp
                entry.userRunRemoteUsage = rec.userRunRemoteUsage
                entry.sysRunRemoteUsage = rec.sysRunRemoteUsage
                entry.userRunLocalUsage = rec.userRunLocalUsage
                entry.sysRunLocalUsage = rec.sysRunLocalUsage
                entry.bytesSent = rec.runBytesSent
                entry.bytesReceived = rec.runBytesReceived
                entry.terminationTime = rec.timestamp
                entry.terminationCode = rec.event
                entry.terminationReason = "Terminated normally"
            elif rec.event == CondorEvents.EvictedEvent:
                fEvicted = True
                entry.executionStopTime = rec.timestamp
                entry.terminationReason = rec.reason
                entry.userRunRemoteUsage = rec.userRunRemoteUsage
                entry.sysRunRemoteUsage = rec.sysRunRemoteUsage
                entry.runBytesSent = rec.runBytesSent 
                entry.runBytesReceived = rec.runBytesReceived
            elif rec.event == CondorEvents.AbortedEvent:
                if entry.terminationReason == None:
                    entry.terminationReason = rec.reason
            elif rec.event == CondorEvents.ShadowExceptionEvent:
                entry.executionStopTime = rec.timestamp
                entry.terminationReason = rec.reason
            elif rec.event == CondorEvents.SocketReconnectFailureEvent:
                # this resubmits, so we create a new record
                entries.append(entry)
                nextEntry = DbRecord()
                nextEntry.condorId = rec.condorId
                nextEntry.dagNode = rec.condorId
                nextEntry.submitTime = rec.timestamp
                entry = nextEntry
        entries.append(entry)
        return entries
