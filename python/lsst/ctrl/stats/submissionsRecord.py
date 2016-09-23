from __future__ import absolute_import
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
from .dbRecord import DbRecord


class SubmissionsRecord(DbRecord):
    """Representation of a "submissions" SQL table row.  Note that the names
    here must match those of the SQL columns.
    """

    def __init__(self, rec=None):
        """
        Constructor
        """
        if rec is None:
            # condor id
            self.condorId = None

            # dag node
            self.dagNode = None

            # time this job was submitted
            self.submitTime = None

            # host this job ran on
            self.executionHost = None

            # time the job started to execute
            self.executionStartTime = "0000-00-00 00:00:00"

            # time the job stopped executing
            self.executionStopTime = "0000-00-00 00:00:00"

            # image size
            self.updateImageSize = 0

            # memory usage in MB
            self.updateMemoryUsageMb = 0

            # resident memory usages in KB
            self.updateResidentSetSizeKb = 0

            # user runtime on remote resource
            self.userRunRemoteUsage = 0

            # sys runtime on remote resource
            self.sysRunRemoteUsage = 0

            # final total of disk usage in KB
            self.finalDiskUsageKb = 0

            # final total of disk requested in KB
            self.finalDiskRequestKb = 0

            # final total of memory usage in MB
            self.finalMemoryUsageMb = 0

            # final total of memory requested in MB
            self.finalMemoryRequestMb = 0

            # bytes sent by job
            self.bytesSent = 0

            # bytes received by job
            self.bytesReceived = 0

            # time the job terminated
            self.terminationTime = "0000-00-00 00:00:00"

            # job termination code
            self.terminationCode = None

            # job termination reason
            self.terminationReason = None

            # slot name for this job
            self.slotName = None
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
            self.finalDiskUsageKb = rec.finalDiskUsageKb
            self.finalDiskRequestKb = rec.finalDiskRequestKb
            self.finalMemoryUsageMb = rec.finalMemoryUsageMb
            self.finalMemoryRequestMb = rec.finalMemoryRequestMb
            self.bytesSent = rec.bytesSent
            self.bytesReceived = rec.bytesReceived
            self.terminationTime = rec.terminationTime
            self.terminationCode = rec.terminationCode
            self.terminationReason = rec.terminationReason
            self.slotName = rec.slotName
