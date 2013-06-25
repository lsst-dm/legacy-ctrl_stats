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
import datetime
import sys
import collections
from collections import defaultdict

class DbStartInfo:
    def __init__(self, info):
        self.dagNode = info[0]
        self.executionHost = info[1]
        self.slotName = info[2]
        self.executionStartTime = info[3]
        self.terminationTime = info[4]
        self.timeToNext = -1

#
# represents which each job was started
#

class NewJobStart:

    def __init__(self, dbm):
        self.dbm = dbm

        query = "select dagNode, executionHost, slotName, UNIX_TIMESTAMP(executionStartTime), UNIX_TIMESTAMP(terminationTime) from submissions where executionStartTime != '0000-00-00 00:00:00' and dagNode != 'A' and dagNode !='B' and slotName !='' order by executionHost, slotName, executionStartTime;"

        results = self.dbm.execCommandN(query)
        self.entries = []
        for res in results:
            startInfo = DbStartInfo(res)
            self.entries.append(startInfo)

    # calculate the length of time from when a worker stopped in a slot until
    # the next worker started
    def calculate(self):
        mylist = []
        for ent in self.entries:
            mylist.append((ent.executionHost+"/"+ent.slotName,[ent.executionStartTime,ent.terminationTime]))
        d = defaultdict(list)
        for k,v in mylist:
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
                for i in range(length-1):
                    #if i == 0:
                    #    print datetime.datetime.fromtimestamp(timeList[0][0]).strftime('%Y-%m-%d %H:%M:%S')
                    timeToNext = timeList[i+1][0] - timeList[i][1]
                    if timeToNext < 0:
                        print "ERROR!"
                        print "length = ",length
                        print "i = ",i
                        print "timeList[i+1][0] = ", timeList[i+1][0]
                        print "timeList[i][1] = ", timeList[i][1]
                        print "timeToNext = ",timeToNext
                        print timeList
                        sys.exit(100)
                    if timeToNext not in totals:
                        totals[timeToNext] = 1
                    else:
                        totals[timeToNext] = totals[timeToNext] + 1
        od = collections.OrderedDict(sorted(totals.items()))
        return od
            

    def consolidate(self):
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
                
