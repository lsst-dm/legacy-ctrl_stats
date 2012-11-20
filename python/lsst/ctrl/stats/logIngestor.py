import eups
import os
import re
from record import Record
from lsst.ctrl.stats.reader import Reader
from lsst.ctrl.stats.classifier import Classifier

class LogIngestor(object):
    """
    Reads a Condor log file, classifies and groups all the records for
    each job, consolidates the information, adds the information to database
    tables.
    """
    def __init__(self, dbm, database):
        self.dbm = dbm

        submissionsTableName = "submissions"
        totalsTableName = "totals"
        updatesTableName = "updates"

        #
        # This load the submissions.sql, which creates the table
        # we're writing into.  The table won't be created
        # if it already exists. (see the SQL for details).

        pkg = eups.productDir("ctrl_stats")

        filePath = os.path.join(pkg,"etc","eventCodes.sql")
        dbm.loadSql(filePath, database)

        filePath = os.path.join(pkg,"etc","submissions.sql")
        dbm.loadSql(filePath, database)

        filePath = os.path.join(pkg,"etc","totals.sql")
        dbm.loadSql(filePath, database)

        filePath = os.path.join(pkg,"etc","updates.sql")
        dbm.loadSql(filePath, database)

        self.submissionsTable = database+"."+submissionsTableName
        self.updatesTable = database+"."+updatesTableName
        self.totalsTable = database+"."+totalsTableName

    def ingest(self, filename):
        # read and parse in the Condor log
        reader = Reader(filename)
        # get the record groups, which are grouped by job
        records = reader.getRecords()

        classifier = Classifier()
        for job in records:
            entries, totalsRecord, updateEntries = classifier.classify(records[job])
            # add submission records
            for ent in entries:
                ins = ent.getInsertString(self.submissionsTable)
                self.dbm.execute(ins)
            # add update records
            for ent in updateEntries:
                ins = ent.getInsertString(self.updatesTable)
                self.dbm.execute(ins)
            # add total entry
            ins = totalsRecord.getInsertString(self.totalsTable)
            self.dbm.execute(ins)

