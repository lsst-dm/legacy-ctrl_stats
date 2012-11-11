#!/usr/bin/env python

import os, sys
from lsst.ctrl.stats.reader import Reader
from lsst.ctrl.stats.classifier import Classifier
from lsst.ctrl.stats.databaseManager import DatabaseManager
from lsst.daf.persistence import DbAuth
from lsst.pex.policy import Policy

if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]
    reader = Reader(sys.argv[3])
    recordList = reader.getRecordList()
    records = recordList.getRecords()

    dbAuth = DbAuth()
    user = dbAuth.username(host, port)
    password = dbAuth.password(host, port)

    dbm = DatabaseManager(host, int(port))
    dbm.connect(user,password,"Testing")

    classifier = Classifier()
    for job in records:
        entries = classifier.classify(records[job])
        for ent in entries:
            ins = ent.getInsertString("Testing.stats")
            print ins
            dbm.execute(ins)
