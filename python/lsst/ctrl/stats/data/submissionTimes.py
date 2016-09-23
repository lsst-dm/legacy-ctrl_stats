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
from future import standard_library
from builtins import object
standard_library.install_aliases()


class SubmissionTimes(object):
    """
    Representation of the submission times of each of the dagNodes
    """

    def __init__(self, dbm):
        """
        This query sorts by submission time, and dagNode.  The dagNode
        needs to be sorted this way because otherwise it comes out A1, A10, A11, A12, A2, A3, A4,
        instead of A1, A2, A3, A4, etc.
        """
        query = "select dagNode, executionHost, slotName, UNIX_TIMESTAMP(submitTime), "
        query = query + "UNIX_TIMESTAMP(executionStartTime), UNIX_TIMESTAMP(executionStopTime), "
        query = query + "UNIX_TIMESTAMP(terminationTime) from submissions order by submitTime, "
        query = query + "length(dagNode), dagNode;"

        results = dbm.execCommandN(query)

        ents = []
        for res in results:
            dbEnt = DbEntry(res)
            ents.append(dbEnt)

        # DBEntries object with submission times of dagNodes
        self.entries = DbEntries(ents)

    def getEntries(self):
        """
        @return DBEntries object with submission times of dagNodes
        """
        return self.entries
