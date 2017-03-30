#!/usr/bin/env python
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

# condorLogIngest - ingest Condor log file(s) into a database
#
# examples:
#
# condorLogIngest.py -H lsst10 -d testing -f worker.log
# condorLogIngest.py -H lsst10 -p 3306 -d testing2 -f worker-pre.log worker.log

from __future__ import print_function
from future import standard_library
from builtins import str
import os
import sys
import argparse
from lsst.ctrl.stats.databaseManager import DatabaseManager
from lsst.ctrl.stats.logIngestor import LogIngestor
from lsst.daf.persistence import DbAuth

standard_library.install_aliases()


if __name__ == "__main__":
    basename = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(prog=basename,
                                     description='''Takes a list of log \
files and ingests them into a database''', epilog='''example:\
condorLogIngest.py -H lsst10 -d testing -f worker.log''')
    parser.add_argument("-H", "--host", action="store", default=None,
                        dest="host", help="mysql server host", type=str,
                        required=True)
    parser.add_argument("-p", "--port", action="store", default=3306,
                        dest="port", help="mysql server port", type=int)
    parser.add_argument("-d", "--database", action="store", default=None,
                        dest="database", help="database name", type=str,
                        required=True)
    parser.add_argument("-m", "--metrics", action="store", default=None,
                        dest="metrics", help="condor log files", type=str,
                        required=True)
    parser.add_argument("-f", "--file", action="store", default=None,
                        dest="filenames", help="condor log files",
                        nargs='+', type=str, required=True)
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                        help="verbose")

    args = parser.parse_args()

    host = args.host
    port = args.port
    database = args.database

    #
    # get database authorization info
    #

    dbAuth = DbAuth()
    user = dbAuth.username(host, str(port))
    password = dbAuth.password(host, str(port))

    # connect to the database
    dbm = DatabaseManager(host, port, user, password)

    # create the database if it doesn't exist
    if not dbm.dbExists(database):
        dbm.createDb(database)

    # create the LogIngestor, which creates all the tables, and will
    # be used to consolidate file information
    logIngestor = LogIngestor(dbm, database)

    # go through the list of files and ingest them, ignoring any
    # that don't exist.
    for filename in args.filenames:
        if not os.path.exists(filename):
            if args.verbose:
                print("warning: %s does not exist." % filename)
            continue
        logIngestor.ingest(args.metrics, filename)
    dbm.close()
