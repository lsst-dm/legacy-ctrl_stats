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
from builtins import object
from future import standard_library
from lsst.ctrl.stats.data.dbEntry import DbEntry
from lsst.ctrl.stats.data.dbEntries import DbEntries
standard_library.install_aliases()


class SuccessTimes(object):
    """Number of successful dagNode completions.

    Parameters
    ----------
    dbm: `DatabaseManager`
        the database manager to use to query
    """

    def __init__(self, dbm):
        query = "select dagNode, executionHost, slotName, \
UNIX_TIMESTAMP(submitTime), UNIX_TIMESTAMP(executionStartTime), \
UNIX_TIMESTAMP(executionStopTime), UNIX_TIMESTAMP(terminationTime) \
from submissions where terminationCode='005';"

        results = dbm.execCommandN(query)

        ents = []
        for res in results:
            dbEnt = DbEntry(res)
            ents.append(dbEnt)

        # DBEntries representing records of successful completions
        self.entries = DbEntries(ents)

    def getEntries(self):
        """
        @return DBEntries representing records of successful completions
        """
        return self.entries
