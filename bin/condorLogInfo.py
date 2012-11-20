#!/usr/bin/env python

#
# debugging utility for Condor log information.   Groups Condor records
# together via the CondorId, and prints them in groups to make it easier
# to see what happened for particular jobs.  This is used for debugging
# the database import scripts, but might be useful for others to see.
#

import argparse
import os
import sys
from lsst.ctrl.stats.reader import Reader

def printRecords(job):
    for rec in records[job]:
            name = rec.__class__.__name__
            if args.verbose:
                print name
                rec.printAll()
            else:
                print name, rec.describe()
    print

if __name__ == "__main__":

    basename = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(prog=basename)
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="verbose")
    parser.add_argument("-c", "--condorid", action="store", default=None, dest="condorIds", help="print only condorId(s)", nargs="+", type=str, required=False)
    parser.add_argument("-f", "--filenames", action="store", default=None, dest="filenames", help="condor log files", nargs="+", type=str, required=True)


    args = parser.parse_args()

    for filename in args.filenames:
        if not os.path.exists(filename):
            if args.verbose:
                print "warning: file %s not found " % filename
            continue
        reader = Reader(filename)
        records = reader.getRecords()
    
        # print all the records
        if args.condorIds is None:
            for job in records:
                printRecords(job)
        else:
            # print only the records with these condorIdss
            for job in args.condorIds:
                if job in records:
                    printRecords(job)
        
