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

# examples:
#
# stats.py -H lsst10 -p 3306 -d testing --submits-per-interval

import os, sys
import datetime
import argparse
from lsst.ctrl.stats.databaseManager import DatabaseManager
from lsst.ctrl.stats.logIngestor import LogIngestor
from lsst.daf.persistence import DbAuth
from lsst.pex.policy import Policy

class DbEntry:

    def __init__(self, dbList):
        self.dagNode = dbList[0]
        self.executionHost = dbList[1]
        self.slotName = dbList[2]
        self.executionStartTime = dbList[3]
        self.executionStopTime = dbList[4]

def run():
    basename = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(prog=basename)
    parser.add_argument("-H", "--host", action="store", default=None, dest="host", help="mysql server host", type=str, required=True)
    parser.add_argument("-p", "--port", action="store", default=3306, dest="port", help="mysql server port", type=int)
    parser.add_argument("-d", "--database", action="store", default=None, dest="database", help="database name", type=str, required=True)
    parser.add_argument("-S", "--submits-per-interval", action="store_true", default=None, dest="submits", help="submits per interval")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="verbose")

    args = parser.parse_args()

    host = args.host
    port = args.port
    database = args.database
    
    #
    # get database authorization info
    #
    dbAuth = DbAuth()
    user = dbAuth.username(host, str(port))
    password = dbAuth.password(host,str(port))

    # connect to the database
    dbm = DatabaseManager(host, port, user, password)


    dbm.execCommand0('use '+database)

    if args.submits == True:
        submissionsPerInterval(dbm)



    # TODO:  Output Start time, End Time, Amount of time preJob takes,
    # first full usage of all cores, drain time from full usage to end,
    # time of last job started to end.
        

def submissionsPerInterval(dbm):
    q0 = 'select submitTime, count(*) as count from submissions group by submitTime;'

    results = dbm.execCommandN(q0)

    for res in results:
        submitTime = res[0]
        count = res[1]
        print "%s, %s" % (submitTime, count)
    

if __name__ == "__main__":
    run()

