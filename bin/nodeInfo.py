#!/usr/bin/env python

import sys
from lsst.ctrl.stats.reader import Reader

if __name__ == "__main__":
    reader = Reader(sys.argv[1])
    flag = sys.argv[2]
    recordList = reader.getRecordList()
    records = recordList.getRecords()

    for job in records:
        for rec in records[job]:
                name = rec.__class__.__name__
                if flag == "full":
                    print name
                    rec.printAll()
                else:
                    print name, rec.describe()
        print "-----"
