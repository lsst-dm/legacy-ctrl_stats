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
from lsst.ctrl.stats.data.dbEntry import DbEntry
from lsst.ctrl.stats.data.dbEntries import DbEntries

class InitialSubmissionTimes:

    def __init__(self, dbm):
        query = "select a.dagNode, a.executionHost, a.slotName, UNIX_TIMESTAMP(a.submitTime), UNIX_TIMESTAMP(a.executionStartTime), UNIX_TIMESTAMP(a.executionStopTime), UNIX_TIMESTAMP(a.terminationTime)  from submissions a inner join ( select dagNode, min(id) minID from submissions group by dagNode) b on a.dagNode = b.dagNode and a.id = b.minId order by a.submitTime, a.id;"
    
        results = dbm.execCommandN(query)
    
        ents = []
        for res in results:
            dbEnt = DbEntry(res)
            ents.append(dbEnt)

        self.entries = DbEntries(ents)
    

    def getEntries(self):
        return self.entries
