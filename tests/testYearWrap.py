#!/usr/bin/env python
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

from builtins import str
import os
import unittest
import lsst.utils.tests
from lsst.ctrl.stats.reader import Reader
from helper.timeutils import utc_tzlocal, add_tzlocal


def setup_module(module):
    lsst.utils.tests.init()


class TestYearWrap(lsst.utils.tests.TestCase):

    def setUp(self):
        pkgDir = os.path.abspath(os.path.dirname(__file__))
        metrics = os.path.join(pkgDir, "testfiles", "year.metrics")
        filename = os.path.join(pkgDir, "testfiles", "year_wrap.log")
        reader = Reader(metrics, filename)
        self.records = reader.getRecords()

    def assertTimeEqual(self, utctimestamp, dateString):
        self.assertEqual(utc_tzlocal(utctimestamp), add_tzlocal(dateString))

    def test1(self):
        # check to see we have the number of records we expect
        self.assertEqual(len(self.records), 5)

    def test2(self):
        # check validity of Submitted record
        self.assertIn("061.000.000", self.records)
        rec = self.records["061.000.000"][0]
        self.assertEqual(rec.__class__.__name__, "Submitted")
        self.assertTimeEqual(rec.utctimestamp, "2016-12-31 19:59:53")
        rec = self.records["061.000.000"][1]
        self.assertEqual(rec.__class__.__name__, "Executing")
        self.assertTimeEqual(rec.utctimestamp, "2016-12-31 19:59:55")
        rec = self.records["061.000.000"][2]
        self.assertEqual(rec.__class__.__name__, "Terminated")
        self.assertTimeEqual(rec.utctimestamp, "2016-12-31 19:59:55")

    def test3(self):
        # check validity of Executing record
        self.assertIn("062.000.000", self.records)
        rec = self.records["062.000.000"][1]
        self.assertEqual(rec.__class__.__name__, "Executing")
        self.assertTimeEqual(rec.utctimestamp, "2016-12-31 19:59:58")

        rec = self.records["062.000.000"][2]
        self.assertEqual(rec.__class__.__name__, "Updated")
        self.assertTimeEqual(rec.utctimestamp, "2017-01-01 20:00:07")

        rec = self.records["062.000.000"][4]
        self.assertEqual(rec.__class__.__name__, "Terminated")
        self.assertTimeEqual(rec.utctimestamp, "2017-01-01 20:00:14")

    def test4(self):
        # check validity of Executing record
        self.assertIn("063.000.000", self.records)
        rec = self.records["063.000.000"][1]
        self.assertEqual(rec.__class__.__name__, "Executing")
        self.assertTimeEqual(rec.utctimestamp, "2016-12-31 20:00:04")

        rec = self.records["063.000.000"][3]
        self.assertEqual(rec.__class__.__name__, "Terminated")
        self.assertTimeEqual(rec.utctimestamp, "2017-01-01 20:00:14")

    def test7(self):
        # check validity of post record
        self.assertIn("065.000.000", self.records)
        rec = self.records["065.000.000"][0]
        self.assertTimeEqual(rec.utctimestamp, "2017-01-01 20:00:16")
        rec = self.records["065.000.000"][1]
        self.assertTimeEqual(rec.utctimestamp, "2017-01-01 20:00:17")
        rec = self.records["065.000.000"][2]
        self.assertTimeEqual(rec.utctimestamp, "2017-01-01 20:00:19")


class ReaderMemoryTestCase(lsst.utils.tests.MemoryTestCase):
    pass


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
