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
import MySQLdb
from dbRecord import DbRecord

class SubmissionsRecord(DbRecord):
    """Representation of a "submissions" SQL table row.  Note that the names
    here must match those of the SQL columns.
    """ 
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
            self.finalDiskUsageKb = 0
            self.finalDiskRequestKb = 0
            self.finalMemoryUsageMb = 0
            self.finalMemoryRequestMb = 0
            self.bytesSent = 0
            self.bytesReceived = 0
            self.terminationTime = "0000-00-00 00:00:00"
            self.terminationCode = None
            self.terminationReason = None
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
