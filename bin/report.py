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
from lsst.ctrl.stats.data.dbEntry import DbEntry
from lsst.ctrl.stats.data.submissionTimes import SubmissionTimes
from lsst.ctrl.stats.data.submitsPerInterval import SubmitsPerInterval
from lsst.ctrl.stats.data.coresPerSecond import CoresPerSecond
from lsst.ctrl.stats.data.executionsPerSlot import ExecutionsPerSlot

def run():
    basename = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(prog=basename)
    parser.add_argument("-H", "--host", action="store", default=None, dest="host", help="mysql server host", type=str, required=True)
    parser.add_argument("-p", "--port", action="store", default=3306, dest="port", help="mysql server port", type=int)
    parser.add_argument("-d", "--database", action="store", default=None, dest="database", help="database name", type=str, required=True)
    parser.add_argument("-I", "--submits-per-interval", action="store_true", default=None, dest="submits", help="number of submits to the condor queue per interval")
    parser.add_argument("-C", "--cores-used-each-second", action="store_true", default=None, dest="cores", help="cores used each second")
    parser.add_argument("-S", "--summary", action="store_true", default=None, dest="summary", help="summary of run")
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

    values = None
    submitTimes = SubmissionTimes(dbm)
    entries = submitTimes.getEntries()
    if args.submits == True:
        submitsPerInterval = SubmitsPerInterval(dbm)
        values = submitsPerInterval.calculate()
        writeValues(values)
    elif args.cores == True:
        coresPerSecond = CoresPerSecond(dbm)
        values = coresPerSecond.calculate(entries)
        writeValues(values)
    elif args.summary == True:
        printSummary(dbm, entries)

def printSummary(dbm, entries):
        print "summary"

        # preJob
        preJob = entries.getPreJob()
        preJobSubmitTime = dateTime(preJob.submitTime)
        preJobStartTime = dateTime(preJob.executionStartTime)
        startTime = preJob.executionStartTime-preJob.submitTime
        runTime = preJob.executionStopTime-preJob.executionStartTime

        print "PreJob submitted %s" % (preJobSubmitTime)
        print "PreJob started %s" % (preJobStartTime)
        print "PreJob time to start: %s" % timeStamp(startTime)
        print "PreJob run duration: %s" % timeStamp(runTime)
        print
        # postJob
        postJob = entries.getPostJob()
        postJobSubmitTime = dateTime(postJob.submitTime)
        postJobStartTime = dateTime(postJob.executionStartTime)
        runTime = postJob.executionStopTime-postJob.executionStartTime
        print "PostJob submitted %s" % (postJobSubmitTime)
        print "PostJob started %s" % (postJobStartTime)
        startTime = postJob.executionStartTime-postJob.submitTime
        print "PostJob time to start: %s" % timeStamp(startTime)
        print "PostJob run duration: %s" % timeStamp(runTime)
        print
        # first worker
        firstWorker = entries.getDagNode('A1')
        print "First worker submitted at %s" % dateTime(firstWorker.submitTime)
        print "First worker started at %s" % dateTime(firstWorker.executionStartTime)

        # last worker
        lastWorker = entries.getLastWorker()
        print "Last worker submitted at %s" % dateTime(lastWorker.submitTime)
        print "Last worker started at %s" % dateTime(lastWorker.executionStartTime)

        # workers overall
        submitDuration = lastWorker.submitTime-firstWorker.submitTime
        print "First worker submit until last worker submit: %s" % timeStamp(submitDuration)

        workerRunTime = lastWorker.executionStartTime-firstWorker.executionStartTime
        print "First worker started to last worker finished: %s" % timeStamp(workerRunTime)
        print


        # Time until maximum cores are used
        coresPerSecond = CoresPerSecond(dbm)
        values = coresPerSecond.calculate(entries)
        maximumCores, timeFirstUsed = maximumCoresFirstUsed(values)
        print "Maximum cores %s first used at %s" % (maximumCores, timeFirstUsed)

        # Executions per Slot
        executionsPerSlot = ExecutionsPerSlot(dbm)
        avg = executionsPerSlot.average()
        min = executionsPerSlot.min()
        max = executionsPerSlot.max()
        print "Average number of executions per slot: %d" % avg
        print "Minimum number of executions per slot: %d" % min
        print "Maximum number of executions per slot: %d" % max


def dateTime(val):
    return datetime.datetime.fromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S')

def timeStamp(val):
    return str(datetime.timedelta(seconds=val))

def maximumCoresFirstUsed(values):
    maximumCores = -1
    timeFirstUsed = None
    for j in range(len(values)):
        val = values[j]
        timeValue = val[0]
        cores = val[1]
        if cores > maximumCores:
            maximumCores = cores
            timeFirstUsed = timeValue
    return maximumCores, timeFirstUsed
       
def writeValues(values):
    if values == None:
        return
    for j in range(len(values)):
        val = values[j]
        length = len(val)
        for i in range(length):
            if (i > 0):
                sys.stdout.write(", ")
            sys.stdout.write("%s" % val[i])
        sys.stdout.write("\n")
    return



    # TODO:  Output Start time, End Time, Amount of time preJob takes,
    # first full usage of all cores, drain time from full usage to end,
    # time of last job started to end.
        

if __name__ == "__main__":
    run()

