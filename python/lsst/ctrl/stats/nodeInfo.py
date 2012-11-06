#!/usr/bin/env python

import sys
from reader import Reader

if __name__ == "__main__":
    reader = Reader(sys.argv[1])
    recordList = reader.getRecordList()
    records = recordList.getRecords()

    for job in records:
        for rec in records[job]:
                name = rec.__class__.__name__
                print name, rec.describe()
        print "-----"
