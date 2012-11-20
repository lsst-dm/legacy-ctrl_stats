#!/usr/bin/env python

import argparse
import os
import sys
from lsst.ctrl.stats.reader import Reader

if __name__ == "__main__":

    basename = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(prog=basename)
    parser.add_argument("-c", "--complete", action="store_true", dest="complete", help="complete log record description")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="verbose")
    parser.add_argument("-f", "--filenames", action="store", default=None, dest="filenames", help="condor log files", nargs="+", type=str, required=True)

    args = parser.parse_args()

    for filename in args.filenames:
        if not os.path.exists(filename):
            if args.verbose:
                print "warning: file %s not found " % filename
            continue
        reader = Reader(filename)
        records = reader.getRecords()
    
        for job in records:
            for rec in records[job]:
                    name = rec.__class__.__name__
                    if args.complete:
                        print name
                        rec.printAll()
                    else:
                        print name, rec.describe()
            print "-----"
