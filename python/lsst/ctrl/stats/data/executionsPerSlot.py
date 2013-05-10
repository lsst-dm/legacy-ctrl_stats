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
import sys
#
# represents the number of times a worker is executing in a particular slot
#
class ExecutionsPerSlot:

    def __init__(self, dbm):
        self.dbm = dbm
        query = "select concat(executionHost, '/', slotName) as slot, count(*) as timesUsed from submissions where dagNode != 'A' and dagNode != 'B' group by executionHost, slotName;"

        self.results = self.dbm.execCommandN(query)

    def average(self):
        avg = 0
        for res in self.results:
            avg = avg + res[1]
        return int(avg/len(self.results)+0.5)
            

    def min(self):
        m = sys.maxint
        for res in self.results:
            if m > res[1]:
                m = res[1]
        return m

    def max(self):
        m = -sys.maxint -1
        for res in self.results:
            if res[1] > m:
                m = res[1]
        return m
