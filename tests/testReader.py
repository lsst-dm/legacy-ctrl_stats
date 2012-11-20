#!/usr/bin/env python
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
import os
import unittest
from lsst.ctrl.stats.reader import Reader
from lsst.ctrl.stats.condorEvents import CondorEvents

class test1(unittest.TestCase):
    def setup(self):
        None

    def test1(self):
        filename = os.path.join("tests","testfiles","reader_test.log")
        reader = Reader(filename)
        records = reader.getRecords()
        self.assertTrue(len(records) == 3)
        self.assertTrue("062.000.000" in records)
        self.assertTrue("063.000.000" in records)
        self.assertTrue("064.000.000" in records)
        rec = records["062.000.000"][0]
        self.assertTrue(rec.__class__.__name__ == "Submitted")
        self.assertTrue(rec.dagNode == "A1")
        self.assertTrue(rec.event == CondorEvents.SubmittedEvent)

        rec = records["062.000.000"][1]
        self.assertTrue(rec.__class__.__name__ == "Executing")
        self.assertTrue(rec.event == CondorEvents.ExecutingEvent)
        self.assertTrue(rec.executingHostAddr == "141.142.225.136:41156")

        rec = records["062.000.000"][2]
        self.assertTrue(rec.__class__.__name__ == "Updated")
        self.assertTrue(rec.event == CondorEvents.UpdatedEvent)
        self.assertTrue(rec.imageSize == 272192)
        self.assertTrue(rec.memoryUsageMb == 40)
        self.assertTrue(rec.residentSetSizeKb == 40640)
        self.assertTrue(rec.timestamp == "2012-10-17 20:00:07")

        rec = records["062.000.000"][3]
        self.assertTrue(rec.__class__.__name__ == "Updated")
        self.assertTrue(rec.event == CondorEvents.UpdatedEvent)

        rec = records["062.000.000"][4]
        self.assertTrue(rec.__class__.__name__ == "Terminated")
        self.assertTrue(rec.event == CondorEvents.TerminatedEvent)
        self.assertTrue(rec.memoryRequest == 40)
        self.assertTrue(rec.memoryUsage == 40)
        self.assertTrue(rec.runBytesReceived == 1449)
        self.assertTrue(rec.runBytesSent == 25594)
        self.assertTrue(rec.sysRunLocalUsage == 0)
        self.assertTrue(rec.sysRunRemoteUsage == 1)
        self.assertTrue(rec.sysTotalLocalUsage == 0)
        self.assertTrue(rec.sysTotalRemoteUsage == 1)
        self.assertTrue(rec.timestamp == "2012-10-17 20:00:14")
        self.assertTrue(rec.totalBytesReceived == 1449)
        self.assertTrue(rec.totalBytesSent == 25594)
        self.assertTrue(rec.userRunLocalUsage == 0)
        self.assertTrue(rec.userRunRemoteUsage == 1)
        self.assertTrue(rec.userTotalLocalUsage == 0)
        self.assertTrue(rec.userTotalRemoteUsage == 1)


if __name__ == "__main__":
    unittest.main()
