# 
# LSST Data Management System
# Copyright 2008-2012 LSST Corporation.
# 
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the LSST License Statement and 
# the GNU General Public License along with this program.  If not, 
# see <http://www.lsstcorp.org/LegalNotices/>.
#
import sys
from condorEvents import CondorEvents
from submissionsRecord import SubmissionsRecord
from totalsRecord import TotalsRecord
from updatesRecord import UpdatesRecord

class Classifier(object):
    """
    Takes a group of records and classifies them into summary groups of
    summary records
    """
    def classify(self, records):

        entries = []
        updateEntries = []

        entry = SubmissionsRecord()

        fExecuting = False
        fEnded = False
        imageSize = 0
        for rec in records:
            if rec.event == CondorEvents.SubmittedEvent:
                entry.condorId = rec.condorId
                entry.dagNode = rec.dagNode
                entry.submitTime = rec.timestamp
            elif rec.event == CondorEvents.ExecutingEvent:
                # only record the first time this is seen for this
                # entry records, since Condor can spit out multiple
                # ExecutingEvents in a row without anything happening
                # (aborts, restarts, etc) in between.  (As per Condor docs).
                if fExecuting is False:
                    entry.executionHost = rec.executingHostAddr
                    entry.executionStartTime = rec.timestamp
                fExecuting = True
            elif rec.event == CondorEvents.UpdatedEvent:
                # create a new update record and fill that in
                updateEntry = UpdatesRecord()
                updateEntry.condorId = entry.condorId
                updateEntry.dagNode = entry.dagNode
                updateEntry.executionHost = entry.executionHost
                updateEntry.timestamp = rec.timestamp
                updateEntry.imageSize = rec.imageSize
                updateEntry.memoryUsageMb = rec.memoryUsageMb
                updateEntry.residentSetSizeKb = rec.residentSetSizeKb
                updateEntries.append(updateEntry)
    
                # update the current records information
                # for this entry
                entry.updateImageSize = rec.imageSize
                entry.updateMemoryUsageMb = rec.memoryUsageMb
                entry.updateResidentSetSizeKb = rec.residentSetSizeKb
            elif rec.event == CondorEvents.TerminatedEvent:
                # termination occurred without some kind of Condor
                # incident.
                entry.executionStopTime = rec.timestamp
                entry.userRunRemoteUsage = rec.userRunRemoteUsage
                entry.sysRunRemoteUsage = rec.sysRunRemoteUsage
                entry.bytesSent = rec.runBytesSent
                entry.bytesReceived = rec.runBytesReceived
                entry.finalDiskUsageKb = rec.diskUsage
                entry.finalDiskRequestKb = rec.diskRequest
                entry.finalMemoryUsageMb = rec.memoryUsage
                entry.finalMemoryRequestMb = rec.memoryRequest
                entry.terminationTime = rec.timestamp
                entry.terminationCode = rec.event
                entry.terminationReason = "Terminated normally"
            elif rec.event == CondorEvents.HeldEvent:
                # the job was held, which means it stopped
                fEnded = True
                entry.terminationCode = rec.event
                entry.terminationTime = rec.timestamp
                entry.terminationReason = rec.reason
            elif rec.event == CondorEvents.EvictedEvent:
                # job was removed, either by condor or the user
                fEnded = True
                entry.terminationTime = rec.timestamp
                entry.terminationCode = rec.event
                entry.terminationReason = rec.reason
                entry.userRunRemoteUsage = rec.userRunRemoteUsage
                entry.sysRunRemoteUsage = rec.sysRunRemoteUsage
                entry.finalDiskUsageKb = rec.diskUsage
                entry.finalDiskRequestKb = rec.diskRequest
                entry.finalMemoryUsageMb = rec.memoryUsage
                entry.finalMemoryRequestMb = rec.memoryRequest
                entry.bytesSent = rec.runBytesSent 
                entry.bytesReceived = rec.runBytesReceived
            elif rec.event == CondorEvents.AbortedEvent:
                # job was aborted
                if not fEnded:
                    if entry.terminationReason == None:
                        entry.terminationReason = rec.reason
                    entry.terminationCode = rec.event
                    entry.terminationTime = rec.timestamp
                fEnded = False
            elif rec.event == CondorEvents.ShadowExceptionEvent:
                # something happened with the shadow daemon, and this
                # job is going to be rescheduled.
                entry.terminationCode = rec.event
                entry.terminationTime = rec.timestamp
                entry.terminationReason = rec.reason
                entries.append(entry)
                nextEntry = SubmissionsRecord()
                nextEntry.condorId = rec.condorId
                nextEntry.dagNode = entry.dagNode
                nextEntry.submitTime = rec.timestamp
                entry = nextEntry
                fExecuting = False
            elif rec.event == CondorEvents.SocketReconnectFailureEvent:
                # lost communication with execution node
                # this resubmits, so we create a new record
                entry.terminationCode = rec.event
                entry.terminationTime = rec.timestamp
                entry.terminationReason = rec.reason
                entries.append(entry)
                nextEntry = SubmissionsRecord()
                nextEntry.condorId = rec.condorId
                nextEntry.dagNode = entry.dagNode
                nextEntry.submitTime = rec.timestamp
                entry = nextEntry
                fExecuting = False
        entries.append(entry)
        totalsRecord = self.tabulate(records, entries)
        return entries, totalsRecord, updateEntries

    def tabulate(self, records, entries):
        # copy the last record
        totalsEntry = TotalsRecord(entries[-1])
        # first submission timestamp
        totalsEntry.firstSubmitTime = entries[0].submitTime
        # total number of submissions
        totalsEntry.submissions = len(entries)

        slotSet = set()
        for rec in entries:
            # global number of bytesSent for this record group
            totalsEntry.totalBytesSent += rec.bytesSent
            # global number of bytesReceived for this record group
            totalsEntry.totalBytesReceived += rec.bytesReceived
            # number of times execution started
            if rec.executionStartTime != "0000-00-00 00:00:00":
                totalsEntry.executions += 1
            # number of times termination occurred because of shadow exceptions
            if rec.terminationCode == CondorEvents.ShadowExceptionEvent:
                totalsEntry.shadowException += 1
            # number of times termination occurred because of socket
            # reconnection failures
            elif rec.terminationCode == CondorEvents.SocketReconnectFailureEvent:
                totalsEntry.socketReconnectFailure += 1
            # if execution occured, add it to the lists of unique hosts
            if rec.executionHost is not None:
                slotSet.add(rec.executionHost)
        # the total number of unique slots used
        totalsEntry.slotsUsed = len(slotSet)
        # the total number of unique hosts used, keeping in mind that one
        # host can have multiple slots
        hostSet = set()
        for slot in slotSet:
            i = slot.index(":")
            hostSet.add(slot[:i])
        totalsEntry.hostsUsed = len(hostSet)

        # the number of SocketLost events
        for rec in records:
            # the number of SocketReconnectionReestablished events
            if rec.event == CondorEvents.SocketReestablishedEvent:
                totalsEntry.socketReestablished += 1
            # the number of SocketLost events
            elif rec.event == CondorEvents.SocketLostEvent:
                totalsEntry.socketLost += 1
            # the number of Evicted Events
            elif rec.event == CondorEvents.EvictedEvent:
                totalsEntry.evicted += 1
            # the number of Aborted Events
            elif rec.event == CondorEvents.AbortedEvent:
                totalsEntry.aborted += 1
        return totalsEntry
