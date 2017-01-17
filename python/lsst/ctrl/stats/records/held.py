#
# LSST Data Management System
# Copyright 2008-2012 LSST Corporation.
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
from __future__ import absolute_import
from .record import Record

# 012 (003.000.000) 07/12 22:36:52 Job was held.
#        Error from slot2@big15.ncsa.illnois.edu: the job manager could not stage out a file
#        Code 2 Subcode 155
# ...


class Held(Record):
    """Job was held

    The job has transitioned to the hold state.
    This might happen if the user applies the "condor_hold" command to the job.

    Parameters
    ----------
    year: `str`
        the year to tag the job with
    lines: list
        the strings making up this record
    """

    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

        pat = r"Error from (?P<slot>[\w@\d\-.]+): (?P<reason>.+?)($)"
        slot, reason = self.extractPair(pat, lines[1], "slot", "reason")
        # slot name
        self.slot = slot
        # reason job was held
        self.reason = reason.strip()

        pat = r"Code (?P<code>[\d]+) Subcode (?P<subcode>[\d]+)"
        code, subcode = self.extractPair(pat, lines[2], "code", "subcode")
        # error code
        self.code = code
        # error subcode
        self.subcode = subcode

    def describe(self):
        """
        @return a string describing the contents of this object
        """
        desc = super(Held, self).describe()
        if desc is None:
            return None
        s = "%s reason=%s" % (self.timestamp, self.reason)
        return s

eventClass = Held
eventCode = "012"
