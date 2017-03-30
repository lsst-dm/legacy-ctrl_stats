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
#
# debugging utility for Condor log information.   Groups Condor records
# together via the CondorId, and prints them in groups to make it easier
# to see what happened for particular jobs.  This is used for debugging
# the database import scripts, but might be useful for others to see.
#

from __future__ import print_function
import argparse
import os
import sys
from lsst.ctrl.stats.reader import Reader


def printRecords(records, job, verbose):
    """ print records for a particular job, optionally in verbose mode"""
    for rec in records[job]:
        name = rec.__class__.__name__
        if verbose:
            rec.printAll()
        else:
            print(name, rec.describe())
    print()


if __name__ == "__main__":

    basename = os.path.basename(sys.argv[0])

    msg = '''example: condorLogInfo.py -c 630.000.000 -f \
srp_2012_0925_160117/*nodes.log'''
    parser = argparse.ArgumentParser(prog=basename,
                                     description='''A debugging utility to \
view record groups.  This is useful in viewing records without having to do a \
complete database ingest.''', epilog=msg)
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                        help="verbose")
    parser.add_argument("-c", "--condorid", action="store", default=None,
                        dest="condorIds", help="print only condorId(s)",
                        nargs="+", type=str, required=False)
    parser.add_argument("-f", "--filenames", action="store", default=None,
                        dest="filenames", help="condor log files", nargs="+",
                        type=str, required=True)

    args = parser.parse_args()

    for filename in args.filenames:
        if not os.path.exists(filename):
            if args.verbose:
                print("warning: file %s not found " % filename)
            continue
        reader = Reader(filename)
        records = reader.getRecords()

        # print all the records
        if args.condorIds is None:
            for job in records:
                printRecords(records, job, args.verbose)
        else:
            # print only the records with these condorIdss
            for job in args.condorIds:
                if job in records:
                    printRecords(records, job, args.verbose)
