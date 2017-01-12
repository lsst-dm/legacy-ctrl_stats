#
# LSST Data Management System
# Copyright 2008-2012 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#
from future import standard_library
from builtins import object
import eups
import os
from lsst.ctrl.stats.reader import Reader
from lsst.ctrl.stats.classifier import Classifier

standard_library.install_aliases()


class LogIngestor(object):
    """
    Reads a Condor log file, classifies and groups all the records for
    each job, consolidates the information, adds the information to database
    tables.
    """

    def __init__(self, dbm, database):
        """Sets up the database tables which will be written to
        @param dbm: a database manager object
        @param database: the database name to write to
        """
        # database object to use for queries
        self.dbm = dbm

        submissionsTableName = "submissions"
        totalsTableName = "totals"
        updatesTableName = "updates"

        #
        # This load the submissions.sql, which creates the table
        # we're writing into.  The table won't be created
        # if it already exists. (see the SQL for details).

        pkg = eups.productDir("ctrl_stats")

        filePath = os.path.join(pkg, "sql", "eventCodes.sql")
        dbm.loadSql(filePath, database)

        filePath = os.path.join(pkg, "sql", "submissions.sql")
        dbm.loadSql(filePath, database)

        filePath = os.path.join(pkg, "sql", "totals.sql")
        dbm.loadSql(filePath, database)

        filePath = os.path.join(pkg, "sql", "updates.sql")
        dbm.loadSql(filePath, database)

        # full name of the submissions table
        self.submissionsTable = database + "." + submissionsTableName
        # full name of the updates table
        self.updatesTable = database + "." + updatesTableName
        # full name of the totals table
        self.totalsTable = database + "." + totalsTableName

    def ingest(self, metrics, filename):
        """Read in a Condor event log, group records per Condor ID,
        consolidate that information, and put it into database tables.
        @param metrics: a Condor metrics file
        @param filename: a Condor event log
        """
        # read and parse in the Condor log
        reader = Reader(metrics, filename)
        # get the record groups, which are grouped by condor id
        records = reader.getRecords()

        classifier = Classifier()
        for job in records:
            entries, totalsRecord, updateEntries = classifier.classify(records[job])
            # add submission records
            for ent in entries:
                cmd, args = ent.getInsertQuery(self.submissionsTable)
                self.dbm.execCommand0(cmd, *args)
            # add update records
            for ent in updateEntries:
                cmd, args = ent.getInsertQuery(self.updatesTable)
                self.dbm.execCommand0(cmd, *args)
            # add total entry
            cmd, args = totalsRecord.getInsertQuery(self.totalsTable)
            self.dbm.execCommand0(cmd, *args)
