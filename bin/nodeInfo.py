#!/usr/bin/env python

import argparse
import sys
from lsst.ctrl.stats.reader import Reader

if __name__ == "__main__":

    basename = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(prog=basename)
    parser.add_argument("-f", "--file", action="store", default=None, dest="filename", help="condor log file", type=str, required=True)
    parser.add_argument("-c", "--complete", action="store_true", dest="complete", help="complete")

    args = parser.parse_args()

    reader = Reader(args.filename)
    recordList = reader.getRecordList()
    records = recordList.getRecords()

    for job in records:
        for rec in records[job]:
                name = rec.__class__.__name__
                if args.complete:
                    print name
                    rec.printAll()
                else:
                    print name, rec.describe()
        print "-----"
