#!/usr/bin/env python

import os, sys
import eups
from lsst.ctrl.stats.reader import Reader
from lsst.ctrl.stats.classifier import Classifier
from lsst.ctrl.stats.databaseManager import DatabaseManager
from lsst.daf.persistence import DbAuth
from lsst.pex.policy import Policy

if __name__ == "__main__":
    tableName = "nodes"

    host = sys.argv[1]
    port = sys.argv[2]
    database = sys.argv[3]
    reader = Reader(sys.argv[4])
    recordList = reader.getRecordList()
    records = recordList.getRecords()

    #
    # get database authorization info
    #
    home = os.getenv("HOME")
    pol = Policy(os.path.join(home,".lsst","db-auth.paf"))
    
    dbAuth = DbAuth()
    dbAuth.setPolicy(pol)
    
    user = dbAuth.username(host,port)
    password = dbAuth.password(host,port)

    print "0"
    dbm = DatabaseManager(host, int(port))
    dbm.connect(user,password)

    print "1"
    if not dbm.dbExists(database):
        print "a"
        dbm.createDb(database) 
        print "b"
    # this second connect is necessary to 
    # connect to the database. It
    # reuses the connection
    dbm.connect(user,password,database)
        

    print "2"
    if not dbm.tableExists(tableName):
        print "a"
        pkg = eups.productDir("ctrl_stats")
        filePath = os.path.join(pkg,"etc","nodes.sql")
        print "b"
        dbm.loadSqlScript(filePath, user, password, database)
    print "3"

    table = database+"."+tableName

    classifier = Classifier()
    for job in records:
        entries = classifier.classify(records[job])
        for ent in entries:
            ins = ent.getInsertString(table)
            print ins
            dbm.execute(ins)
