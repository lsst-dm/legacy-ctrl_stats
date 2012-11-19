#!/usr/bin/env python

import os, sys
import eups
import argparse
from lsst.ctrl.stats.reader import Reader
from lsst.ctrl.stats.classifier import Classifier
from lsst.ctrl.stats.databaseManager import DatabaseManager
from lsst.daf.persistence import DbAuth
from lsst.pex.policy import Policy

if __name__ == "__main__":
    submissionsTableName = "submissions"
    totalsTableName = "totals"
    updatesTableName = "updates"

    basename = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(prog=basename)
    parser.add_argument("-H", "--host", action="store", default=None, dest="host", help="mysql host", type=str, required=True)
    parser.add_argument("-p", "--port", action="store", default=None, dest="port", help="mysql port", type=str, required=True)
    parser.add_argument("-d", "--database", action="store", default=None, dest="database", help="database name", type=str, required=True)
    parser.add_argument("-f", "--file", action="store", default=None, dest="filenames", help="condor log file", nargs='+', type=str, required=True)
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="verbose")

    args = parser.parse_args()

    host = args.host
    port = args.port
    database = args.database

    print args.filenames
    if args.verbose:
        for filename in args.filenames:
            if not os.path.exists(filename):
                print "warning: %s does not exist." % filename
    
    #
    # get database authorization info
    #
    home = os.getenv("HOME")
    pol = Policy(os.path.join(home,".lsst","db-auth.paf"))
    
    dbAuth = DbAuth()
    user = dbAuth.username(host, port)
    password = dbAuth.password(host, port)

    dbm = DatabaseManager(host, int(port))
    dbm.connect(user,password)

    if not dbm.dbExists(database):
        dbm.createDb(database) 
    # this second connect is necessary to 
    # connect to the database. It
    # reuses the connection.
    dbm.connect(user,password,database)
        
    #
    # This load the submissions.sql, which creates the table
    # we're writing into.  The table won't be created
    # if it already exists. (see the SQL for details).

    pkg = eups.productDir("ctrl_stats")

    filePath = os.path.join(pkg,"etc","eventCodes.sql")
    dbm.loadSqlScript(filePath, user, password, database)

    filePath = os.path.join(pkg,"etc","submissions.sql")
    dbm.loadSqlScript(filePath, user, password, database)

    filePath = os.path.join(pkg,"etc","totals.sql")
    dbm.loadSqlScript(filePath, user, password, database)

    filePath = os.path.join(pkg,"etc","updates.sql")
    dbm.loadSqlScript(filePath, user, password, database)

    submissionsTable = database+"."+submissionsTableName
    totalsTable = database+"."+totalsTableName
    updatesTable = database+"."+updatesTableName


    for filename in args.filenames:
        if not os.path.exists(filename):
            continue
        # read and parse in the Condor log
        reader = Reader(filename)
        # get the record groups, which are grouped by job
        records = reader.getRecords()
    
        classifier = Classifier()
        for job in records:
            entries, totalsRecord, updateEntries = classifier.classify(records[job])
            # add submission records
            for ent in entries:
                ins = ent.getInsertString(submissionsTable)
                if args.verbose:
                    print ins
                dbm.execute(ins)
            # add update records
            for ent in updateEntries:
                ins = ent.getInsertString(updatesTable)
                if args.verbose:
                    print ins
                dbm.execute(ins)
            # add total entry
            ins = totalsRecord.getInsertString(totalsTable)
            if args.verbose:
                print ins
            dbm.execute(ins)
