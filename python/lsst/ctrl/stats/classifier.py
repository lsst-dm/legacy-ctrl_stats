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

from __future__ import absolute_import
from builtins import object
from .submissionsRecord import SubmissionsRecord
from .totalsRecord import TotalsRecord
from .updatesRecord import UpdatesRecord
import lsst.ctrl.stats.records as recordslib


class Classifier(object):
    """Takes a group of Condor event records and classifies them into
    groups of summary records
    """

    def createUpdatesRecord(self, entry, rec):
        """Create a new UpdatesRecord and fill it in
        @param entry: an entry to update
        @param rec: a record containing new information
        @return: the new updated entry
        """
        updateEntry = UpdatesRecord()
        updateEntry.condorId = entry.condorId
        updateEntry.dagNode = entry.dagNode
        updateEntry.executionHost = entry.executionHost
        updateEntry.timestamp = rec.timestamp
        updateEntry.imageSize = rec.imageSize
        updateEntry.memoryUsageMb = rec.memoryUsageMb
        updateEntry.residentSetSizeKb = rec.residentSetSizeKb
        updateEntry.slotName = entry.slotName
        return updateEntry

    def recordTermination(self, entry, rec):
        """Record fields after we've received a termination record
        @param entry: an entry to fill in
        @param rec: a record containing information
        """
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

    def recordEviction(self, entry, rec):
        """Record eviction  information
        @param entry: an entry to fill in
        @param rec: a record containing information
        """
        self.recordTerminationInfo(entry, rec)
        entry.userRunRemoteUsage = rec.userRunRemoteUsage
        entry.sysRunRemoteUsage = rec.sysRunRemoteUsage
        entry.finalDiskUsageKb = rec.diskUsage
        entry.finalDiskRequestKb = rec.diskRequest
        entry.finalMemoryUsageMb = rec.memoryUsage
        entry.finalMemoryRequestMb = rec.memoryRequest
        entry.bytesSent = rec.runBytesSent
        entry.bytesReceived = rec.runBytesReceived

    def recordShadowExceptionInfo(self, entry, rec):
        """Record shadow exception record information
        @param entry: an entry to fill in
        @param rec: a record containing information
        """
        self.recordTerminationInfo(entry, rec)
        entry.bytesSent = rec.runBytesSent
        entry.bytesReceived = rec.runBytesReceived

    def updateJobInformation(self, entry, rec):
        """Update entry with record's information
        @param entry: an entry to fill in
        @param rec: a record containing information
        """
        entry.updateImageSize = rec.imageSize
        entry.updateMemoryUsageMb = rec.memoryUsageMb
        entry.updateResidentSetSizeKb = rec.residentSetSizeKb

    def recordTerminationInfo(self, entry, rec):
        """Record termination information
        @param entry: an entry to fill in
        @param rec: a record containing information
        """
        entry.terminationCode = rec.event
        entry.terminationTime = rec.timestamp
        entry.terminationReason = rec.reason

    def createResubmissionRecord(self, entry, rec):
        """Create a new record containing termination information
        @param entry: an entry to fill in
        @param rec: a record containing information
        @return a new SubmissionsRecord
        """
        newRec = SubmissionsRecord()
        newRec.condorId = rec.condorId
        newRec.dagNode = entry.dagNode
        newRec.submitTime = rec.timestamp
        return newRec

    def classify(self, records):
        """Classify a list of Condor event records into secondary
        database records, recording statistics about data in the list.
        @param records: list containing Condor event records
        @return: list of submissions, a totalsRecord and a list of updates
        @return entries, totalsRecord, updateEntries
        """

        entries = []
        updateEntries = []

        entry = SubmissionsRecord()

        fExecuting = False
        fEnded = False
        for rec in records:
            if rec.event == recordslib.jobAdInformation.eventCode:
                entry.slotName = rec.slotName
            elif rec.event == recordslib.submitted.eventCode:
                entry.condorId = rec.condorId
                entry.dagNode = rec.dagNode
                entry.submitTime = rec.timestamp
            elif rec.event == recordslib.executing.eventCode:
                # Only record the first time this is seen for this
                # entry records, since Condor can spit out multiple
                # ExecutingEvents in a row without anything happening
                # (aborts, restarts, etc) in between.  (As per Condor docs).
                if fExecuting is False:
                    entry.executionHost = rec.executingHostAddr
                    entry.executionStartTime = rec.timestamp
                fExecuting = True
            elif rec.event == recordslib.updated.eventCode:
                updateEntry = self.createUpdatesRecord(entry, rec)
                updateEntries.append(updateEntry)

                self.updateJobInformation(entry, rec)
            elif rec.event == recordslib.terminated.eventCode:
                # termination occurred without some kind of Condor
                # incident.
                self.recordTermination(entry, rec)
            elif rec.event == recordslib.held.eventCode:
                # the job was held, which effectively means it stopped,
                # in our context
                fEnded = True
                self.recordTerminationInfo(entry, rec)
            elif rec.event == recordslib.evicted.eventCode:
                # job was removed, either by condor or the user,
                # and this job will be rescheduled.
                self.recordEviction(entry, rec)
                entry = self.resubmit(entries, entry, rec)
                fExecuting = False
            elif rec.event == recordslib.aborted.eventCode:
                # job was aborted
                if not fEnded:
                    if entry.terminationReason is None:
                        entry.terminationReason = rec.reason
                    entry.terminationCode = rec.event
                    entry.terminationTime = rec.timestamp
                fEnded = False
            elif rec.event == recordslib.shadowException.eventCode:
                # something happened with the shadow daemon, and this
                # job is going to be rescheduled.
                self.recordShadowExceptionInfo(entry, rec)
                entry = self.resubmit(entries, entry, rec)
                fExecuting = False
            elif rec.event == recordslib.socketReconnectFailure.eventCode:
                # lost communication with execution node
                # this resubmits, so we create a new record
                self.recordTerminationInfo(entry, rec)
                entry = self.resubmit(entries, entry, rec)
                fExecuting = False
        entries.append(entry)
        totalsRecord = self.tabulate(records, entries)
        return entries, totalsRecord, updateEntries

    def resubmit(self, entries, entry, rec):
        """Store the current entry, and return a new resubmission record
        @param entries: a list of summary "submissions" records for the database
        @param entry: the current submission entry record
        @param rec: the current record
        @return: a new entry record
        """
        entries.append(entry)
        newEntry = self.createResubmissionRecord(entry, rec)
        return newEntry

    def tabulate(self, records, entries):
        """
        Tabulate all the information in records and entires into one record
        @param records: a list of Condor Event Records
        @param entries: a list of summary "submissions" records for the database
        @return: a record intended for the "totals" table in the database
        """
        # copy the last record, and use that as a starting point
        totalsEntry = TotalsRecord(entries[-1])
        # first submission timestamp
        totalsEntry.firstSubmitTime = entries[0].submitTime
        # total number of submissions
        totalsEntry.submissions = len(entries)

        slotSet = set()
        slotName = None
        for ent in entries:
            # global number of bytesSent for this record group
            totalsEntry.totalBytesSent += ent.bytesSent
            # global number of bytesReceived for this record group
            totalsEntry.totalBytesReceived += ent.bytesReceived
            # number of times execution started
            if ent.executionStartTime != "0000-00-00 00:00:00":
                totalsEntry.executions += 1
            # number of times termination occurred because of shadow exceptions
            if ent.terminationCode == recordslib.shadowException.eventCode:
                totalsEntry.shadowException += 1
            # number of times termination occurred because of socket
            # reconnection failures
            elif ent.terminationCode == recordslib.socketReconnectFailure.eventCode:
                totalsEntry.socketReconnectFailure += 1
            # if execution occured, add it to the lists of unique hosts
            if ent.executionHost is not None:
                slotSet.add(ent.executionHost)
            slotName = ent.slotName
        # the total number of unique slots used
        totalsEntry.slotsUsed = len(slotSet)
        # Last named slot used is the successful one
        # (This isn't necessarily the last entry in "entries", i.e., it's
        # not "entries[=1]"; it's the last time we saw a slot name).
        totalsEntry.slotName = slotName
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
            if rec.event == recordslib.socketReestablished.eventCode:
                totalsEntry.socketReestablished += 1
            # the number of SocketLost events
            elif rec.event == recordslib.socketLost.eventCode:
                totalsEntry.socketLost += 1
            # the number of Evicted Events
            elif rec.event == recordslib.evicted.eventCode:
                totalsEntry.evicted += 1
            # the number of Aborted Events
            elif rec.event == recordslib.aborted.eventCode:
                totalsEntry.aborted += 1
        return totalsEntry
