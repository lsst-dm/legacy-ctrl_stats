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
    def __init__(self, year, lines):
        self.lines = list(lines)

        pat = r"(?P<event>\d+) " + \
            r"\((?P<condorId>.+?.)\) " + \
            r"(?P<month>\d+)\/(?P<day>\d+) " + \
            r"(?P<timestamp>\d+:\d+:\d+) "

        info = re.search(pat,lines[0])
        values = {}
        if info is not None:
            values = info.groupdict()
            self.event = values["event"]
            self.condorId = values["condorId"]
            self.timestamp = str(year)+"-"+values["month"]+"-"+values["day"]+" "+values["timestamp"]
        else:
            print "error parsing record:"
            print lines[0]
            sys.exit(10)

    def printAll(self):
        print "class name = %s " % self.__class__.__name__
        members = [attr for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__")]
        for mem in members:
            value = getattr(self, mem)
            print mem, "=", value


    def extractValues(self,pat,line):
        try:
            values = re.search(pat,line).groupdict()
            return values
        except AttributeError:
            print "exiting"
            sys.exit(100)

    def extract(self,pat,line,tag):
        values = re.search(pat,line).groupdict()
        val = values[tag]
        return val

    def extractPair(self, pat, line, tag1, tag2):
        values = self.extractValues(pat, line)
        val1 = values[tag1]
        val2 = values[tag2]
        return val1, val2

    def extractUsageRequest(self, line):
        input = line.strip()

        usage = 0
        request = 0

        pat = r":\s+(?P<usage>\d+)\s+(?P<request>\d+)$"
        values = re.search(pat,input)
        if values is not None:
            val1, val2 = self.extractPair(pat,input,"usage","request")
            usage = int(val1)
            request = int(val2)
        else:
            pat = r":\s+(?P<request>\d+)$"
            request = int(self.extract(pat,input,"request"))
        return usage, request

    def extractUsrSysTimes(self, line):
        pat = r"Usr \d+ " + \
                r"(?P<usrHours>\d+):(?P<usrMinutes>\d+):(?P<usrSeconds>\d+), "  + \
                r"Sys \d+ " + \
                r"(?P<sysHours>\d+):(?P<sysMinutes>\d+):(?P<sysSeconds>\d+) "
        values = self.extractValues(pat,line)
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
        s = "%s %s %s" % (self.event, self.condorId, self.timestamp)
        return s

    def str(self):
        return "%s, %s" % (self.__class__.__name__,rec.timestamp)
