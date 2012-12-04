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
from collections import OrderedDict
import itertools
class RecordList(object):
    """An ordered list of Record objects
    """
    def __init__(self):
        self.records = OrderedDict()

    def append(self, rec):
        """Append a record to the list of records corresponding to it's 
        Condor ID
        @param rec: a Condor event record object
        """
        #condorId = rec.condorId
        #if self.records.has_key(condorId):
        #    recordGroup = self.records[condorId]
        #    recordGroup.append(rec)
        #else:
        #    recordGroup = []
        #    recordGroup.append(rec)
        #    self.records[condorId] = recordGroup
        self.records.get(rec.condorId, []).append(rec)
        print self.records

    def getRecords(self):
        """Accessor which returns all the record lists
        """
        return self.records

    def printAll(self):
        """print long representations of all the records in groups according
        to Condor Id
        """
        for i in self.records:
            
           for rec in self.records[i]:
                print i, rec
           print
        for i in self.records:
            print i 
            for rec in self.records[i]:
                print rec.printAll()

    def printGroups(self):
        """print brief representations of all the records in groups according
        to Condor Id
        """
        for i in self.records:
            
           for rec in self.records[i]:
                print i, rec
           print
