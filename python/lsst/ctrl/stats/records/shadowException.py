from __future__ import absolute_import
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
import re
from .record import Record

#
# 007 (010.000.000) 10/22 13:54:20 Shadow exception!
#     Error from slot3@lsst15.ncsa.illinois.edu: Failed to execute '/tmp/srp/big.sh' with arguments 20 21 22: (errno=8: 'Exec format error')
#     0  -  Run Bytes Sent By Job
#     0  -  Run Bytes Received By Job
# ...


class ShadowException(Record):
    """
    Shadow exception
    The "condor_shadow", a program on the submit computer taht watches over
    the job and performs some services for the job, failed for some 
    catastrophic reason..  The job will leave the machine and go back into
    the queue.
    """

    def __init__(self, year, lines):
        """
        Constructor
        @param year - the year to tag the job with
        @param lines - the strings making up this record
        """
        Record.__init__(self, year, lines)

        pat = r"Error from (?P<slot>[\w]+@[\d]+@[\w\-.]+): (?P<reason>.+?)($)"
        ## the slot the job was in at the time of this exception
        self.slot = None
        ## the reason for the exception
        self.reason = None
        ## the number of bytes sent
        self.runBytesSent = None
        ## the number of bytes received
        self.runBytesReceived = None
        if re.search(pat, lines[1]) is not None:
            values = self.extractValues(pat, lines[1])
            self.slot = values["slot"]
            self.reason = values["reason"].strip()
            pat = r"(?P<bytes>\d+) "
            self.runBytesSent = int(self.extract(pat, lines[2], "bytes"))
            self.runBytesReceived = int(self.extract(pat, lines[3], "bytes"))
        else:
            self.reason = lines[1].strip()
            pat = r"(?P<bytes>[\d]+)"
            self.runBytesSent = int(self.extract(pat, lines[2], "bytes"))
            self.runBytesReceived = int(self.extract(pat, lines[3], "bytes"))

eventClass = ShadowException
eventCode = "007"
