from __future__ import print_function
from builtins import str
from builtins import object
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
import sys


class Record(object):
    """
    Representation of a HTCondor record
    """

    def __init__(self, year, lines):
        """
        Constructor
        @param year - the year to tag the job with
        @param lines - the strings making up this record
        """
        # strings making up this record
        self.lines = list(lines)

        pat = r"(?P<event>\d+) " + \
            r"\((?P<condorId>.+?.)\) " + \
            r"(?P<month>\d+)\/(?P<day>\d+) " + \
            r"(?P<timestamp>\d+:\d+:\d+) "

        info = re.search(pat, lines[0])
        values = {}
        if info is not None:
            values = info.groupdict()
            # the event type
            self.event = values["event"]
            # the condor id
            self.condorId = values["condorId"]
            # the timestamp
            self.timestamp = str(year)+"-"+values["month"]+"-"+values["day"]+" "+values["timestamp"]
        else:
            print("error parsing record:")
            print(lines[0])
            sys.exit(10)

    def printAll(self):
        """
        print a description of this record to the console
        """
        print("class name = %s " % self.__class__.__name__)
        members = [attr for attr in dir(self) if not callable(
            getattr(self, attr)) and not attr.startswith("__")]
        for mem in members:
            value = getattr(self, mem)
            print(mem, "=", value)

    def extractValues(self, pat, line):
        """
        Extract all values given a pattern and line
        @param pat pattern to match
        @param line to extract values from
        @return a dictionary of extracted values
        """
        try:
            values = re.search(pat, line).groupdict()
            return values
        except AttributeError:
            print("exiting")
            sys.exit(100)

    def extract(self, pat, line, tag):
        """
        Extract a single value from a line
        @param pat pattern to match
        @param line to extract values from
        @param tag the specific tag to extract
        @return the extracted tag value
        """
        values = re.search(pat, line).groupdict()
        val = values[tag]
        return val

    def extractPair(self, pat, line, tag1, tag2):
        """
        Extract two values from a line
        @param pat pattern to match
        @param line to extract values from
        @param tag1 a tag to extract
        @param tag2 a tag to extract
        @return the extracted tag values
        """
        values = self.extractValues(pat, line)
        val1 = values[tag1]
        val2 = values[tag2]
        return val1, val2

    def extractUsageRequest(self, line):
        """
        extract usage request information from a line
        @return usage and request fields
        """
        input = line.strip()

        usage = 0
        request = 0

        pat = r":\s+(?P<usage>\d+)\s+(?P<request>\d+)$"
        values = re.search(pat, input)
        if values is not None:
            val1, val2 = self.extractPair(pat, input, "usage", "request")
            usage = int(val1)
            request = int(val2)
        else:
            pat = r":\s+(?P<request>\d+)$"
            request = int(self.extract(pat, input, "request"))
        return usage, request

    def extractUsageRequestAllocated(self, line):
        """
        extract usage request information from a line
        @return usage request and allocated fields
        """
        input = line.strip()
        usage = 0
        request = 0
        allocated = 0
        pat = r":\s+(?P<usage>\d+)\s+(?P<request>\d+)\s+(?P<allocated>\d+)$"
        values = re.search(pat, input)
        if values is not None:
            d = values.groupdict()
            usage = int(d["usage"])
            request = int(d["request"])
            allocated = int(d["allocated"])
        return usage, request, allocated

    def extractUsrSysTimes(self, line):
        """
        extract time from a line
        @return usr and sys fields, computed in seconds
        """
        pat = r"Usr \d+ (?P<usrHours>\d+):(?P<usrMinutes>\d+):(?P<usrSeconds>\d+), "
        pat = pat + r"Sys \d+ (?P<sysHours>\d+):(?P<sysMinutes>\d+):(?P<sysSeconds>\d+) "
        values = self.extractValues(pat, line)
        usrHours = values["usrHours"]
        usrMinutes = values["usrMinutes"]
        usrSeconds = values["usrSeconds"]
        sysHours = values["sysHours"]
        sysMinutes = values["sysMinutes"]
        sysSeconds = values["sysSeconds"]
        usr = int(usrHours)*3600+int(usrMinutes)*60+int(usrSeconds)
        sys = int(sysHours)*3600+int(sysMinutes)*60+int(sysSeconds)
        return usr, sys

    def describe(self):
        """
        Describe this record
        @return a string describing the event, condor id and time stamp
        """
        s = "%s %s %s" % (self.event, self.condorId, self.timestamp)
        return s

    def str(self):
        """
        Describe this record
        @return a string describing this object type and time stamp
        """
        return "%s, %s" % (self.__class__.__name__, self.rec.timestamp)
