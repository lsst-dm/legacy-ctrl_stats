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

class DbEntry(object):
    """A representation of a single database query

    Parameters
    ----------
    dbList : list
        The elements are strings expected in the following sequence:

        dbList[0] - the dag node name
        dbList[1] - the host where the job executed
        dbList[2] - the name of the slot where the job ran
        dbList[3] - the time the job was submitted to HTCondor
        dbList[4] - the time the job started execution
        dbList[5] - the time the job ended execution
        dbList[6] - the time the job was terminated
    """

    def __init__(self, dbList):

        self.dagNode = dbList[0]

        self.executionHost = dbList[1]

        self.slotName = dbList[2]

        if dbList[3] == 0:
            self.submitTime = None
        else:
            self.submitTime = dbList[3]

        if dbList[4] == 0:
            self.executionStartTime = None
        else:
            self.executionStartTime = dbList[4]

        if dbList[5] == 0:
            self.executionStopTime = None
        else:
            self.executionStopTime = dbList[5]

        if dbList[6] == 0:
            self.terminationTime = None
        else:
            self.terminationTime = dbList[6]
