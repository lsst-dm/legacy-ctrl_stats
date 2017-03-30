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
from __future__ import print_function
from builtins import range
from builtins import object
import sys
import collections
from collections import defaultdict


class DbStartInfo(object):
    """Starting record of a job

    Parameters
    ----------
    info: list
        The list has the following sequence
        info[0] - name of DAG node
        info[1] - host job executed on
        info[2] - name of the slot which ran this job
        info[3] - time of start of execution
        info[4] - time of termination of execution
    """

    def __init__(self, info):
        self.dagNode = info[0]
        self.executionHost = info[1]
        self.slotName = info[2]
        self.executionStartTime = info[3]
        self.terminationTime = info[4]

        # time the next execution started in this slot
        self.timeToNext = -1


class NewJobStart(object):
    """Represents when each job was started

    Parameters
    ----------
    dbm: `DatabaseManager`
        the database manager to use to query
    """

    def __init__(self, dbm):
        self.dbm = dbm

        query = "select dagNode, executionHost, slotName, \
UNIX_TIMESTAMP(executionStartTime), UNIX_TIMESTAMP(terminationTime) \
from submissions where executionStartTime != 0 and dagNode != 'A' and \
dagNode !='B' and slotName !='' order by executionHost, slotName, \
executionStartTime;"

        results = self.dbm.execCommandN(query)
        # list of DBStartInfo record representing the results of the new
        # job start query
        self.entries = []
        for res in results:
            startInfo = DbStartInfo(res)
            self.entries.append(startInfo)

    def calculate(self):
        """
        calculate the length of time from when a worker stopped in a slot
        until the next worker started
        """
        mylist = []
        for ent in self.entries:
            mylist.append((ent.executionHost + "/"+ent.slotName,
                          [ent.executionStartTime, ent.terminationTime]))
        d = defaultdict(list)
        for k, v in mylist:
            d[k].append(v)

        totals = {}
        for item in d:
            timeList = d[item]
            length = len(timeList)
            if length == 1:
                if -1 not in totals:
                    totals[-1] = 1
                else:
                    totals[-1] = totals[-1] + 1
            else:
                for i in range(length - 1):
                    timeToNext = timeList[i + 1][0] - timeList[i][1]
                    if timeToNext < 0:
                        print("ERROR! invalid data in the submissions table")
                        sys.exit(100)
                    if timeToNext not in totals:
                        totals[timeToNext] = 1
                    else:
                        totals[timeToNext] = totals[timeToNext] + 1
        od = collections.OrderedDict(sorted(totals.items()))
        return od

    def consolidate(self):
        """
        Consolidate the information and sort the information.
        """
        totals = {}
        for ent in self.entries:
            if ent.secondsTilNext is None:
                continue
            if ent.secondsTilNext not in totals:
                totals[ent.secondsTilNext] = 1
            else:
                totals[ent.secondsTilNext] = totals[ent.secondsTilNext] + 1
        od = collections.OrderedDict(sorted(totals.items()))
        return od
