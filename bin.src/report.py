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

# examples:
#
# report.py -H lsst10 -p 3306 -d testing

from __future__ import print_function
from __future__ import division
from future import standard_library
from builtins import str
import os
import sys
import argparse
from lsst.ctrl.stats.databaseManager import DatabaseManager
from lsst.daf.persistence import DbAuth
from lsst.ctrl.stats.data.submissionTimes import SubmissionTimes
from lsst.ctrl.stats.data.submitsPerInterval import SubmitsPerInterval
from lsst.ctrl.stats.data.slotsPerSecond import SlotsPerSecond
from lsst.ctrl.stats.data.slotsPerInterval import SlotsPerInterval

from lsst.ctrl.stats.report import Report

standard_library.install_aliases()


def report():
    basename = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(prog=basename,
                                     description='''A statistics reporting utility.  Use to print
                            out information about what happened during a run.
                            Takes as an argument previously ingested run
                            information one of the ingest utilities  in
                            a named database.''',
                                     epilog='''example:
report.py -H kaboom.ncsa.illinois.edu -p 3303 -d srp_2013_0601_140432 -S''')
    parser.add_argument("-H", "--host", action="store", default=None,
                        dest="host", help="mysql server host", type=str,
                        required=True)
    parser.add_argument("-p", "--port", action="store", default=3306,
                        dest="port", help="mysql server port", type=int)
    parser.add_argument("-d", "--database", action="store", default=None,
                        dest="database", help="database name", type=str,
                        required=True)
    parser.add_argument("-I", "--submits-per-interval", action="store_true",
                        default=None, dest="submits",
                        help="number of submits to queue per interval")
    parser.add_argument("-S", "--slots-used-each-second", action="store_true",
                        default=None, dest="slots",
                        help="slots used each second")

    parser.add_argument("-N", "--slots-used-each-interval", type=int,
                        default=-1, dest="interval",
                        help="slots used each interval")

    parser.add_argument("-L", "--local-time-zone", action="store_true",
                        default=False, dest="localTimeZone",
                        help="output dates converted to local time zone")

    parser.add_argument("-v", "--verbose", action="store_true",
                        dest="verbose", help="verbose")

    args = parser.parse_args()

    host = args.host
    port = args.port
    database = args.database

    #
    # get database authorization info
    #
    dbAuth = DbAuth()
    user = dbAuth.username(host, str(port))
    password = dbAuth.password(host, str(port))

    # connect to the database
    dbm = DatabaseManager(host, port, user, password)

    dbm.execCommand0('use '+database)

    # command line arguments
    values = None
    submitTimes = SubmissionTimes(dbm)
    entries = submitTimes.getEntries()
    r = Report(dbm, args.localTimeZone)
    if args.submits:
        submitsPerInterval = SubmitsPerInterval(dbm, 1)
        values = submitsPerInterval.getValues()
        r.writePerTimeIntervals(values)
    elif args.slots:
        slotsPerSecond = SlotsPerSecond(dbm, entries)
        values = slotsPerSecond.getValues()
        r.writePerTimeIntervals(values)
    elif args.interval > -1:
        slotsPerInterval = SlotsPerInterval(dbm, entries, args.interval)
        values = slotsPerInterval.getValues()
        r.writePerTimeIntervals(values)
    else:
        printSummary(r)
    dbm.close()


def printSummary(report):
    report.initialJobs()
    report.firstSubmittedJob()
    report.firstExecutingJob()
    report.lastExecutingJob()
    report.lastSubmittedJob()
    report.jobOverall()
    report.allRunTimes()
    report.successfulRunTimes()
    report.slotUtilization()
    report.executionSwitchover()
    report.executionsPerSlot()
    report.totals()


if __name__ == "__main__":
    report()
