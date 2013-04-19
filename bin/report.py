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
from lsst.ctrl.stats.data.workerTotal import WorkerTotal
from lsst.ctrl.stats.data.dbEntry import DbEntry
from lsst.ctrl.stats.data.submissionTimes import SubmissionTimes
from lsst.ctrl.stats.data.initialSubmissionTimes import InitialSubmissionTimes
from lsst.ctrl.stats.data.successTimes import SuccessTimes
from lsst.ctrl.stats.data.submitsPerInterval import SubmitsPerInterval
from lsst.ctrl.stats.data.coresPerSecond import CoresPerSecond
from lsst.ctrl.stats.data.coresPerInterval import CoresPerInterval
from lsst.ctrl.stats.data.executionsPerSlot import ExecutionsPerSlot
from lsst.ctrl.stats.data.firstExecutingWorker import FirstExecutingWorker
from lsst.ctrl.stats.data.lastExecutingWorker import LastExecutingWorker
from lsst.ctrl.stats.data.newJobStart import NewJobStart
from lsst.ctrl.stats.data.terminationStatus import TerminationStatus
from lsst.ctrl.stats.data.executingWorkers import ExecutingWorkers
from lsst.ctrl.stats.data.coreUtilization import CoreUtilization

def run():
    basename = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(prog=basename)
    parser.add_argument("-H", "--host", action="store", default=None, dest="host", help="mysql server host", type=str, required=True)
    parser.add_argument("-p", "--port", action="store", default=3306, dest="port", help="mysql server port", type=int)
    parser.add_argument("-d", "--database", action="store", default=None, dest="database", help="database name", type=str, required=True)
    parser.add_argument("-I", "--submits-per-interval", action="store_true", default=None, dest="submits", help="number of submits to the condor queue per interval")
    parser.add_argument("-C", "--cores-used-each-second", action="store_true", default=None, dest="cores", help="cores used each second")
    parser.add_argument("-N", "--cores-used-each-interval", type=int, default=-1, dest="interval", help="cores used each interval")
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
        submitsPerInterval = SubmitsPerInterval(dbm, 5)
        values = submitsPerInterval.getValues()
        writeDateValues(values)
    elif args.cores == True:
        coresPerSecond = CoresPerSecond(dbm, entries)
        # TODO: fix this
        values = coresPerSecond.getValues()
        writeDateValues(values)
    elif args.interval > -1:
        coresPerInterval = CoresPerInterval(dbm,entries, args.interval)
        values = coresPerInterval.getValues()
        writeDateValues(values)
    elif args.summary == True:
        printSummary(dbm, entries)

def printCoreRampUpRampDownSummary(dbm, entries, initialSubmits, executingWorkers):
    # Time until maximum cores are used
    coresPerSecond = CoresPerSecond(dbm, entries)
    maximumCores = coresPerSecond.getMaximumCores()
    maxCoresFirstUsed = coresPerSecond.maximumCoresFirstUsed()
    maxCoresLastUsed = coresPerSecond.maximumCoresLastUsed()

    initialEntries = initialSubmits.getEntries()
    initialFirstWorker = initialEntries.getFirstWorker()

    firstExecutingWorker = executingWorkers.getFirstExecutingWorker()
    lastExecutingWorker = executingWorkers.getLastExecutingWorker()

    print "Maximum cores %s first used: %s" % (maximumCores, dateTime(maxCoresFirstUsed))
    print "Maximum cores %s last used: %s" % (maximumCores, dateTime(maxCoresLastUsed))
    print "Maximum cores last used until last worker finished: %s" % timeStamp(lastExecutingWorker.executionStopTime-maxCoresLastUsed)
    print "First worker submit to maximum cores used: %s" % timeStamp(maxCoresFirstUsed-initialFirstWorker.submitTime)
    print "First executing worker to maximum cores used: %s" % timeStamp(maxCoresFirstUsed-firstExecutingWorker.executionStartTime)
    print

def printCoreUtilizationSummary(dbm, initialSubmits):
    cu = CoreUtilization(dbm)
    cores = cu.coresUtilized()

    initialEntries = initialSubmits.getEntries()
    initialFirstWorker = initialEntries.getFirstWorker()

    print "Maximum number of cores used: %d" % cores
    print "Time until %d cores are used at least once: %s" % (cores, timeStamp(cu.getLastTime() - cu.getFirstTime()))
    print "First worker submit to %d cores used at least once: %s" % (cores, timeStamp(cu.getLastTime()-initialFirstWorker.submitTime))
    print
    

def printPreJobSummary(dbm, entries):
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

def printPostJobSummary(dbm, entries):
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

def printSummary(dbm, entries):
    executingWorkers = ExecutingWorkers(dbm)

    printPreJobSummary(dbm, entries)

    printPostJobSummary(dbm, entries)

    initialSubmits = InitialSubmissionTimes(dbm)
    initialEntries = initialSubmits.getEntries()
    initialFirstWorker = initialEntries.getFirstWorker()
    initialLastWorker = initialEntries.getLastWorker()
    submissionDuration = initialLastWorker.submitTime-initialLastWorker.submitTime

    count = initialEntries.getLength()-2 # don't count preJob and postJob
    submissionDuration = initialLastWorker.submitTime-initialFirstWorker.submitTime
    print "Total worker submits: %d" % count
    print "Mean initial worker submissions per second: %d" % (count/float(submissionDuration))
    print

    # first worker
    delay = initialFirstWorker.submitTime-entries.getPreJobExecutionStopTime()
    print "Delay of end of preJob to submission of first worker: %s" % timeStamp(delay)
    print "Initial submission - first worker %s submitted at %s" % (initialFirstWorker.dagNode, dateTime(initialFirstWorker.submitTime))
    print "Initial submission - last worker %s submitted at %s" % (initialLastWorker.dagNode, dateTime(initialLastWorker.submitTime))
    print "Initial submission - first worker to last worker submitted: %s" % timeStamp(submissionDuration)


        
    # first executing worker is not necessarily the first 
    # worker submitted, so look it up
    firstExecutingWorker = executingWorkers.getFirstExecutingWorker()

    print "First executing worker %s started at %s" % (firstExecutingWorker.dagNode, dateTime(firstExecutingWorker.executionStartTime))
    print "First executing worker %s stopped at %s" % (firstExecutingWorker.dagNode, dateTime(firstExecutingWorker.executionStopTime))
    print "First executing worker %s run duration %s" % (firstExecutingWorker.dagNode, timeStamp(firstExecutingWorker.executionStopTime-firstExecutingWorker.executionStartTime))
    print


    # last worker in the list
    lastWorker = entries.getLastWorker()
    print "Last submitted worker %s submitted at %s" % (lastWorker.dagNode, dateTime(lastWorker.submitTime))
    print "Last submitted worker %s started executing at %s" % (lastWorker.dagNode, dateTime(lastWorker.executionStartTime))
    print "Last submitted worker %s stopped executing at %s" % (lastWorker.dagNode, dateTime(lastWorker.executionStopTime))
    print "Last submitted worker %s run duration %s" % (lastWorker.dagNode, timeStamp(lastWorker.executionStopTime-lastWorker.executionStartTime))
    print

    # last executing worker is not necessarily the last worker that was
    # submitted.  It's the last worker that was executing at the end of the
    # run.
    worker = LastExecutingWorker(dbm)
    lastExecutingWorker = worker.calculate()
    print "Last executing worker %s started at: %s " % (lastExecutingWorker.dagNode, dateTime(lastExecutingWorker.executionStartTime))
    print "Last executing worker %s finished at: %s " % (lastExecutingWorker.dagNode, dateTime(lastExecutingWorker.executionStopTime))
    print "Last executing worker %s run duration %s" % (lastExecutingWorker.dagNode, timeStamp(lastExecutingWorker.executionStopTime-lastExecutingWorker.executionStartTime))

    # workers overall
    submitDuration = lastWorker.submitTime-initialFirstWorker.submitTime
    print "First executing worker submit until last executing worker submit: %s" % timeStamp(submitDuration)

    workerRunTime = lastExecutingWorker.executionStopTime-firstExecutingWorker.executionStartTime
    print "First executing worker started to last executing worker finished: %s" % (timeStamp(workerRunTime))
    delay = entries.getPostJobSubmitTime() - lastExecutingWorker.executionStopTime
    print "Delay of end of last executing worker %s to submission of postJob: %s" % (lastExecutingWorker.dagNode, timeStamp(delay))
    print

    # run times
    min, max, avg = jobRunTimes(entries)
    print "Minimum submitted worker run time: %s" % timeStamp(min)
    print "Maximum submitted worker run time: %s" % timeStamp(max)
    print "Mean submitted worker run time: %s" % timeStamp(avg)

    successTimes = SuccessTimes(dbm)
    successEntries = successTimes.getEntries()

    min, max, avg = jobRunTimes(successEntries)
    print "Minimum successful worker run time: %s" % timeStamp(min)
    print "Maximum successful worker run time: %s" % timeStamp(max)
    print "Mean successful worker run time: %s" % timeStamp(avg)

    #printCoreRampUpRampDownSummary(dbm, entries, initialSubmits, executingWorkers)
    printCoreUtilizationSummary(dbm, initialSubmits)

    # Executions per Slot
    executionsPerSlot = ExecutionsPerSlot(dbm)
    avg = executionsPerSlot.average()
    min = executionsPerSlot.min()
    max = executionsPerSlot.max()
    print "Minimum executions per slot: %d" % min
    print "Maximum executions per slot: %d" % max
    print "Mean executions per slot: %d" % avg
    print

    newJobStart = NewJobStart(dbm)
    totals = newJobStart.calculate()
    #totals = newJobStart.consolidate()

    
    print "Time from the end of one worker until the next worker starts."
    totalStarts = 0
    totalMinutes = 0
    for key,value in totals.iteritems():
        print "%d second%s until next worker started: %d worker%s total" % (key, 's' if key > 1 else '', value, 's' if value > 1 else '')
        totalStarts = totalStarts + value
        totalMinutes = totalMinutes + key*value
    print "Mean time to next worker start: %.2f seconds" % (totalMinutes/float(totalStarts))

    print

    submittedWorkers = WorkerTotal(dbm)
    print "Total submitted workers: %d" % submittedWorkers.getTotal("submissions")
    successfulWorkers = WorkerTotal(dbm)
    print "Total successful workers: %d" % submittedWorkers.getTotal("totals")
    print
    termStatus = TerminationStatus(dbm)
    totals = termStatus.getTotals()
    for t in totals:
        print "%s: %s" % (t[0],t[1])
        
def dateTime(val):
    return datetime.datetime.fromtimestamp(val).strftime('%Y-%m-%d %H:%M:%S')

def timeStamp(val):
    return str(datetime.timedelta(seconds=val))

def jobRunTimes(ents):
    workers = 0
    totalRunTime = 0
    maxRunTime = - sys.maxint -1
    minRunTime = sys.maxint
    length = ents.getLength()
    for i in range(length):
        ent = ents.getEntry(i)
        if ent.dagNode == 'A':
            continue
        if ent.dagNode == 'B':
            continue
        if ent.executionStartTime == 0:
            continue
        workers = workers + 1
        runTime = ent.terminationTime - ent.executionStartTime
        totalRunTime = totalRunTime+runTime
        if runTime < minRunTime:
            minRunTime = runTime
        if runTime > maxRunTime:
            maxRunTime = runTime;

    if workers > 0:
        avg = totalRunTime/workers
    else:
        avg = 0
        
    return minRunTime, maxRunTime, avg


def writeValues(values):
    if values == None:
        return
    for j in range(len(values)):
        val = values[j]
        length = len(val)
        for i in range(length):
            if (i > 0):
                sys.stdout.write(", %s" % val[i])
            elif i == 0:
                sys.stdout.write("%s" % val[0])
        sys.stdout.write("\n")
    return
       
def writeDateValues(values):
    if values == None:
        return
    for j in range(len(values)):
        val = values[j]
        length = len(val)
        for i in range(length):
            if (i > 0):
                sys.stdout.write(", %s" % val[i])
            elif i == 0:
                sys.stdout.write("%s" % dateTime(val[0]))
        sys.stdout.write("\n")
    return



    # TODO:  Output Start time, End Time, Amount of time preJob takes,
    # first full usage of all cores, drain time from full usage to end,
    # time of last job started to end.
        

if __name__ == "__main__":
    run()

