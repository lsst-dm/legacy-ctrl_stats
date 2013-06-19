# 
# LSST Data Management System
# Copyright 2008-2013 LSST Corporation.
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

#
# a representation of the of the database entries for a given run
#
class DbEntries:

    def __init__(self, entries):
        self.entries = entries

    def getEntry(self, x):
        return self.entries[x]

    def getDagNode(self, dagNode):
        for ent in self.entries:
            if ent.dagNode == dagNode:
                return ent
        return None
    
    def getPreJob(self):
        return self.getDagNode('A')

    def getPreJobExecutionStopTime(self):
        ent = self.getDagNode('A')
        return ent.executionStopTime
    
    def getPostJob(self):
        return self.getDagNode('B')

    def getLength(self):
        return len(self.entries)

    def getFirstWorker(self):
        return self.getDagNode('A1')

    def getLastWorker(self):
        return self.entries[-2]

    def getPostJobSubmitTime(self):
        ent = self.getPostJob()
        if ent == None:
            return None
        return ent.submitTime
