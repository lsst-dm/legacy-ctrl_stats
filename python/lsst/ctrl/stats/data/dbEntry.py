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
# a representation of a single database query
#
class DbEntry:

    def __init__(self, dbList):
        self.dagNode = dbList[0]
        self.executionHost = dbList[1]
        self.slotName = dbList[2]
        self.submitTime = dbList[3]
        self.executionStartTime = dbList[4]
        self.executionStopTime = dbList[5]
        self.terminationTime = dbList[6]
