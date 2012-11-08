#!/usr/bin/env python

import sys
from lsst.ctrl.stats.reader import Reader
from lsst.ctrl.stats.classifier import Classifier

if __name__ == "__main__":
    reader = Reader(sys.argv[1])
    recordList = reader.getRecordList()
    records = recordList.getRecords()

    classifier = Classifier()
    for job in records:
        entries = classifier.classify(records[job])
