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
from builtins import range
from builtins import object


class CoresPer(object):
    """
    Base class to use by the CoresPer* classes
    """

    def __init__(self):
        """
        Constructor
        """
        # the maximum number of cores
        self.maximumCores = -1
        # the time the core was first used
        self.timeFirstUsed = None
        # the time the core was last used
        self.timeLastUsed = None

    def calculateMax(self):
        """
        count the number of cores used at maximum
        also calculate the first time that many cores were used
        and the last time that many cores were used.
        """
        self.maximumCores = -1
        self.timeFirstUsed = None
        self.timeLastUsed = None
        for j in range(len(self.values)):
            val = self.values[j]
            timeValue = val[0]
            cores = val[1]
            # this counts the times the maximum cores
            # were first used
            if cores > self.maximumCores:
                self.maximumCores = cores
                self.timeFirstUsed = timeValue
            # this extra conditional also tallies the
            # last time all the cores were used
            if cores == self.maximumCores:
                self.timeLastUsed = timeValue
        return self.maximumCores, self.timeFirstUsed, self.timeLastUsed

    def getValues(self):
        """
        returns generic values for the subclass
        """
        return self.values

    def getMaximumCores(self):
        """
        returns maximum number of cores utilitized
        """
        return self.maximumCores

    def maximumCoresFirstUsed(self):
        """
        returns the time the maximum number of cores were being utilitized
        """
        return self.timeFirstUsed

    def maximumCoresLastUsed(self):
        """
        returns the last time the maximum number of cores were being utilitized
        """
        return self.timeLastUsed
