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


class SlotsPer(object):
    """
    Base class to use by the SlotsPer* classes
    """

    def __init__(self):
        # the maximum number of slots
        self.maximumSlots = -1
        # the time the slot was first used
        self.timeFirstUsed = None
        # the time the slot was last used
        self.timeLastUsed = None

    def calculateMax(self):
        """
        count the number of slots used at maximum
        also calculate the first time that many slots were used
        and the last time that many slots were used.
        """
        self.maximumSlots = -1
        self.timeFirstUsed = None
        self.timeLastUsed = None
        for j in range(len(self.values)):
            val = self.values[j]
            timeValue = val[0]
            slots = val[1]
            # this counts the times the maximum slots
            # were first used
            if slots > self.maximumSlots:
                self.maximumSlots = slots
                self.timeFirstUsed = timeValue
            # this extra conditional also tallies the
            # last time all the slots were used
            if slots == self.maximumSlots:
                self.timeLastUsed = timeValue
        return self.maximumSlots, self.timeFirstUsed, self.timeLastUsed

    def getValues(self):
        """
        returns generic values for the subclass
        """
        return self.values

    def getMaximumSlots(self):
        """
        returns maximum number of slots utilitized
        """
        return self.maximumSlots

    def maximumSlotsFirstUsed(self):
        """
        returns the time the maximum number of slots were being utilitized
        """
        return self.timeFirstUsed

    def maximumSlotsLastUsed(self):
        """
        returns the last time the maximum number of slots were being utilitized
        """
        return self.timeLastUsed
