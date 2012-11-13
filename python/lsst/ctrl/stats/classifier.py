import sys
from condorEvents import CondorEvents
from nodesRecord import NodesRecord

class Classifier(object):
    def classify(self, records):
        entries = []

        entry = NodesRecord()

        fExecuting = False
        fEnded = False
        imageSize = 0
        for rec in records:
            if rec.event == CondorEvents.SubmittedEvent:
                entry.condorId = rec.condorId
                entry.dagNode = rec.dagNode
                entry.submitTime = rec.timestamp
            elif rec.event == CondorEvents.ExecutingEvent:
                if fExecuting is False:
                    entry.executionHost = rec.executingHostAddr
                    entry.executionStartTime = rec.timestamp
                fExecuting = True
            elif rec.event == CondorEvents.UpdatedEvent:
               entry.imageSize = rec.imageSize
               entry.memoryUsageMB = rec.memoryUsageMB
               entry.residentSetSize = rec.residentSetSize
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
            elif rec.event == CondorEvents.HeldEvent:
                fEnded = True
                entry.terminationCode = rec.event
                entry.terminationTime = rec.timestamp
                entry.terminationReason = rec.reason
            elif rec.event == CondorEvents.EvictedEvent:
                fEnded = True
                entry.terminationTime = rec.timestamp
                entry.terminationCode = rec.event
                entry.terminationReason = rec.reason
                entry.userRunRemoteUsage = rec.userRunRemoteUsage
                entry.sysRunRemoteUsage = rec.sysRunRemoteUsage
                entry.bytesSent = rec.runBytesSent 
                entry.bytesReceived = rec.runBytesReceived
            elif rec.event == CondorEvents.AbortedEvent:
                if not fEnded:
                    if entry.terminationReason == None:
                        entry.terminationReason = rec.reason
                    entry.terminationCode = rec.event
                    entry.terminationTime = rec.timestamp
                fEnded = False
            elif rec.event == CondorEvents.ShadowExceptionEvent:
                entry.terminationCode = rec.event
                entry.terminationTime = rec.timestamp
                entry.terminationReason = rec.reason
                entries.append(entry)
                nextEntry = NodesRecord()
                nextEntry.condorId = rec.condorId
                nextEntry.dagNode = entry.dagNode
                nextEntry.submitTime = rec.timestamp
                entry = nextEntry
                fExecuting = False
            elif rec.event == CondorEvents.SocketReconnectFailureEvent:
                # this resubmits, so we create a new record
                entry.terminationCode = rec.event
                entry.terminationTime = rec.timestamp
                entry.terminationReason = rec.reason
                entries.append(entry)
                nextEntry = NodesRecord()
                nextEntry.condorId = rec.condorId
                nextEntry.dagNode = entry.dagNode
                nextEntry.submitTime = rec.timestamp
                entry = nextEntry
                fExecuting = False
        entries.append(entry)
        return entries
