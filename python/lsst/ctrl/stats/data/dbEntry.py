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


class DbEntry:
    """
    A representation of a single database query
    """

    def __init__(self, dbList):
        """
        Constructor
        """
        ## the DAG node name
        self.dagNode = dbList[0]
        ## the host where the job resided
        self.executionHost = dbList[1]
        ## the name of the slot
        self.slotName = dbList[2]
        ## the time the job was submitted to HTCondor
        self.submitTime = dbList[3]
        ## the time the job started execution
        self.executionStartTime = dbList[4]
        ## the time the job ended execution
        self.executionStopTime = dbList[5]
        ## the time the job was terminated
        self.terminationTime = dbList[6]
