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


class TerminationStatus(object):
    """Representation of how all jobs ended, based on termination codes

    Parameters
    ----------
    dbm: `DatabaseManager`
        the database manager to use to query
    """

    def __init__(self, dbm):
        self.dbm = dbm

    def getTotals(self):
        """
        Return the number of times job termination events occurred.
        @return list containing event type, number of occurrences pairs
        """
        query = "select eventCodes.EventName, (select count(*) from submissions where "
        query = query + "submissions.terminationCode = eventCodes.eventCode and submissions.dagNode "
        query = query + "!= 'A' and submissions.dagNode != 'B') as appears from eventCodes"

        results = self.dbm.execCommandN(query)

        totals = []
        for r in results:
            if r[1] > 0:
                totals.append([r[0], r[1]])

        return totals
