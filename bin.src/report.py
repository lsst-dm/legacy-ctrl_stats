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
# report.py -H lsst10 -p 3306 -d testing -S

from __future__ import print_function
from __future__ import division
from future import standard_library
from builtins import str
from builtins import range
import os
import sys
import datetime
import argparse
import lsst.log as log
import lsst.utils
from lsst.ctrl.stats.databaseManager import DatabaseManager
from lsst.daf.persistence import DbAuth
from lsst.ctrl.stats.data.workerTotal import WorkerTotal
from lsst.ctrl.stats.data.submissionTimes import SubmissionTimes
from lsst.ctrl.stats.data.successTimes import SuccessTimes
from lsst.ctrl.stats.data.submitsPerInterval import SubmitsPerInterval
from lsst.ctrl.stats.data.coresPerSecond import CoresPerSecond
from lsst.ctrl.stats.data.coresPerInterval import CoresPerInterval
from lsst.ctrl.stats.data.executionsPerSlot import ExecutionsPerSlot
from lsst.ctrl.stats.data.newJobStart import NewJobStart
from lsst.ctrl.stats.data.terminationStatus import TerminationStatus
from lsst.ctrl.stats.data.executingWorkers import ExecutingWorkers
from lsst.ctrl.stats.data.coreUtilization import CoreUtilization

standard_library.install_aliases()


def run():
    basename = os.path.basename(sys.argv[0])

    parser = argparse.ArgumentParser(prog=basename,
                                     description='''A statistics reporting utility.  Use to print
                            out information about what happened during a run.
                            Takes as an argument previously ingested run
                            information one of the ingest utilities  in
                            a named database.''',
                                     epilog='''example:
report.py -H kaboom.ncsa.illinois.edu -p 3303 -d srp_2013_0601_140432 -S''')
    parser.add_argument("-H", "--host", action="store", default=None, dest="host",
                        help="mysql server host", type=str, required=True)
    parser.add_argument("-p", "--port", action="store", default=3306,
                        dest="port", help="mysql server port", type=int)
    parser.add_argument("-d", "--database", action="store", default=None,
                        dest="database", help="database name", type=str, required=True)
    parser.add_argument("-I", "--submits-per-interval", action="store_true", default=None,
                        dest="submits", help="number of submits to the condor queue per interval")
    parser.add_argument("-C", "--cores-used-each-second", action="store_true",
                        default=None, dest="cores", help="cores used each second")
    parser.add_argument("-N", "--cores-used-each-interval", type=int, default=-
                        1, dest="interval", help="cores used each interval")
    parser.add_argument("-S", "--summary", action="store_true",
                        default=None, dest="summary", help="summary of run")
    parser.add_argument("-v", "--verbose", action="store_true", dest="verbose", help="verbose")

    args = parser.parse_args()

    package = lsst.utils.getPackageDir("ctrl_stats")
    configPath = os.path.join(package, "etc", "log4j.properties")
    log.configure(configPath)

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

    dbm.execCommand0('use '+database)

    # command line arguments
    values = None
    submitTimes = SubmissionTimes(dbm)
    entries = submitTimes.getEntries()
    if args.submits:
        submitsPerInterval = SubmitsPerInterval(dbm, 1)
        values = submitsPerInterval.getValues()
        writeDateValues(values)
    elif args.cores:
        coresPerSecond = CoresPerSecond(dbm, entries)
        values = coresPerSecond.getValues()
        writeDateValues(values)
    elif args.interval > -1:
        coresPerInterval = CoresPerInterval(dbm, entries, args.interval)
        values = coresPerInterval.getValues()
        writeDateValues(values)
    elif args.summary:
        printSummary(dbm, entries)


def printCoreUtilizationSummary(dbm, entries):
    cu = CoreUtilization(dbm)
    cores = cu.coresUtilized()

    initialFirstWorker = entries.getFirstWorker()

    print("Maximum number of cores used: %d" % cores)
    stamp = timeStamp(cu.getLastTime() - cu.getFirstTime())
    print("Time until %d cores are used at least once: %s" % (cores, stamp))
    stamp = timeStamp(cu.getLastTime()-initialFirstWorker.submitTime)
    print("First worker submit to %d cores used at least once: %s" % (cores, stamp))
    print()


def printPreJobSummary(dbm, entries):
    # preJob
    preJob = entries.getPreJob()
    preJobSubmitTime = dateTime(preJob.submitTime)
    preJobStartTime = dateTime(preJob.executionStartTime)
    startTime = preJob.executionStartTime-preJob.submitTime
    runTime = preJob.executionStopTime-preJob.executionStartTime

    print("PreJob submitted %s" % (preJobSubmitTime))
    print("PreJob started %s" % (preJobStartTime))
    print("PreJob time to start: %s" % timeStamp(startTime))
    print("PreJob run duration: %s" % timeStamp(runTime))
    print()


def printPostJobSummary(dbm, entries):
    # postJob
    postJob = entries.getPostJob()
    if postJob is None:
        print("PostJob not executed")
        print()
        return
    postJobSubmitTime = dateTime(postJob.submitTime)
    postJobStartTime = dateTime(postJob.executionStartTime)
    runTime = postJob.executionStopTime-postJob.executionStartTime
    print("PostJob submitted %s" % (postJobSubmitTime))
    print("PostJob started %s" % (postJobStartTime))
    startTime = postJob.executionStartTime-postJob.submitTime
    print("PostJob time to start: %s" % timeStamp(startTime))
    print("PostJob run duration: %s" % timeStamp(runTime))
    print()


def printSummary(dbm, entries):
    executingWorkers = ExecutingWorkers(dbm)

    printPreJobSummary(dbm, entries)

    printPostJobSummary(dbm, entries)

    initialFirstWorker = entries.getFirstWorker()
    initialLastWorker = entries.getLastWorker()
    submissionDuration = initialLastWorker.submitTime-initialLastWorker.submitTime

    # don't count preJob and postJob, so subtract 2
    count = entries.getLength() - 2

    print("Total worker submits: %d" % count)
    if submissionDuration > 0:
        print("Mean initial worker submissions per second: %d" % (count/submissionDuration))
    else:
        print("Initial workers all submitted at the same time")
    print()

    # first worker
    delay = initialFirstWorker.submitTime-entries.getPreJobExecutionStopTime()
    print("Delay of end of preJob to submission of first worker: %s" % timeStamp(delay))

    # initial submission here means all the workers that got submitted so that all nodes were occupied

    node = initialFirstWorker.dagNode
    submitTime = dateTime(initialFirstWorker.submitTime)
    print("Initial submission - first worker %s submitted at %s" % (node, submitTime))

    node = initialLastWorker.dagNode
    submitTime = dateTime(initialLastWorker.submitTime)
    print("Initial submission - last worker %s submitted at %s" % (node, submitTime))

    print("Initial submission - first worker to last worker submitted: %s" % timeStamp(submissionDuration))

    # first executing worker is not necessarily the first
    # worker submitted, so look it up
    firstExecutingWorker = executingWorkers.getFirstExecutingWorker()

    dagNode = firstExecutingWorker.dagNode
    startTime = firstExecutingWorker.executionStartTime
    stopTime = firstExecutingWorker.executionStopTime
    if startTime is None:
        print("warning: First executing worker has not set start time")
    if stopTime is None:
        print("warning: First executing worker has not set stop time")
    if startTime is not None and stopTime is not None:
        print("First executing worker %s started at %s" % (dagNode, dateTime(startTime)))
        print("First executing worker %s stopped at %s" % (dagNode, dateTime(stopTime)))
        print("First executing worker %s run duration %s" % (dagNode, timeStamp(stopTime-startTime)))
    print()

    # last worker in the list
    lastWorker = entries.getLastWorker()
    dagNode = lastWorker.dagNode
    startTime = lastWorker.executionStartTime
    stopTime = lastWorker.executionStopTime

    if startTime is None:
        print("warning: Last submitted worker has not set start time")
    if stopTime is None:
        print("warning: Last submitted worker has not set stop time")
    
    if startTime is not None and stopTime is not None:
        print("Last submitted worker %s submitted at %s" % (dagNode, dateTime(lastWorker.submitTime)))
        print("Last submitted worker %s started executing at %s" % (dagNode, dateTime(startTime)))
        print("Last submitted worker %s stopped executing at %s" % (dagNode, dateTime(stopTime)))
        print("Last submitted worker %s run duration %s" % (dagNode, timeStamp(stopTime-startTime)))
    print()

    # last executing worker is not necessarily the last worker that was
    # submitted.  It's the last worker that was executing at the end of the
    # run.
    lastExecutingWorker = executingWorkers.getLastExecutingWorker()
    dagNode = lastExecutingWorker.dagNode
    startTime = lastExecutingWorker.executionStartTime
    stopTime = lastExecutingWorker.executionStopTime
    print("Last executing worker %s started at: %s " % (dagNode, dateTime(startTime)))
    print("Last executing worker %s finished at: %s " % (dagNode, dateTime(stopTime)))
    print("Last executing worker %s run duration %s" % (dagNode, timeStamp(stopTime-startTime)))

    # workers overall
    submitDuration = lastWorker.submitTime-initialFirstWorker.submitTime
    print("First executing worker submit until last executing worker submit: %s" % timeStamp(submitDuration))

    workerRunTime = lastExecutingWorker.executionStopTime-firstExecutingWorker.executionStartTime
    print("First executing worker started to last executing worker finished: %s" % (timeStamp(workerRunTime)))
    postTime = entries.getPostJobSubmitTime()
    if postTime is None:
        print()
        print("Could not calculate delay of end of last executing worker")
        print("to submission of postJob, because postJob did not execute.")
    else:
        node = lastExecutingWorker.dagNode
        delay = timeStamp(postTime - lastExecutingWorker.executionStopTime)
        print("Delay of end of last executing worker %s to submission of postJob: %s" % (node, delay))
    print()

    # run times
    min, max, avg = jobRunTimes(entries)
    print("Minimum submitted worker run time: %s" % timeStamp(min))
    print("Maximum submitted worker run time: %s" % timeStamp(max))
    print("Mean submitted worker run time: %s" % timeStamp(avg))
    print()
    successTimes = SuccessTimes(dbm)
    successEntries = successTimes.getEntries()

    min, max, avg = jobRunTimes(successEntries)
    print("Minimum successful worker run time: %s" % timeStamp(min))
    print("Maximum successful worker run time: %s" % timeStamp(max))
    print("Mean successful worker run time: %s" % timeStamp(avg))
    print()

    printCoreUtilizationSummary(dbm, entries)

    # Executions per Slot
    executionsPerSlot = ExecutionsPerSlot(dbm)
    avg = executionsPerSlot.average()
    min = executionsPerSlot.min()
    max = executionsPerSlot.max()
    print("Minimum executions per slot: %d" % min)
    print("Maximum executions per slot: %d" % max)
    print("Mean executions per slot: %d" % avg)
    print()

    newJobStart = NewJobStart(dbm)
    totals = newJobStart.calculate()

    # execution switch over
    if len(list(totals)) == 0:
        print("Could not calculate execution times between workers because")
        print("no valid entries were found.  Check to see if workers were")
        print("executed, and/or if valid slot names were set.")
        print()
    else:
        print("Time from the end of one worker until the next worker starts")
        totalStarts = 0
        totalMinutes = 0
        for key, value in totals.items():
            if key == -1:
                print("Single worker started: %d worker%s total" % (value, 's' if value > 1 else ''))
            else:
                pS = 's' if key > 1 else ''
                pW = 's' if value > 1 else ''
                print("%d second%s until next worker started: %d worker%s total" % (key, pS, value, pW))
                totalMinutes = totalMinutes + key*value
                totalStarts = totalStarts + value
        if totalStarts == 0:
            print("No workers scheduled for more than one slot")
        else:
            print("Mean time to next worker start: %.2f seconds" % (totalMinutes/totalStarts))

        print()

    # totals
    submittedWorkers = WorkerTotal(dbm)
    print("Total submitted workers: %d" % submittedWorkers.getTotal("submissions"))
    successfulWorkers = WorkerTotal(dbm)
    print("Total successful workers: %d" % successfulWorkers.getTotal("totals"))
    print()
    termStatus = TerminationStatus(dbm)
    totals = termStatus.getTotals()
    for t in totals:
        print("%s: %s" % (t[0], t[1]))

# return a formatted date string


def dateTime(val):
    if val == None:
        timeVal = 0
    else:
        timeVal = val
    return datetime.datetime.fromtimestamp(timeVal).strftime('%Y-%m-%d %H:%M:%S')

# return the number of seconds


def timeStamp(val):
    return str(datetime.timedelta(seconds=val))


def jobRunTimes(ents):
    workers = 0
    totalRunTime = 0
    maxRunTime = - sys.maxsize - 1
    minRunTime = sys.maxsize
    length = ents.getLength()
    for i in range(length):
        ent = ents.getEntry(i)
        # ignore preJob, postJob, and jobs that don't start
        if ent.dagNode == 'A':
            continue
        if ent.dagNode == 'B':
            continue
        if ent.executionStartTime == 0:
            continue
        workers = workers + 1
        if ent.terminationTime is None:
            print("warning: job termination time is invalid.")
            runTime = 0
        elif ent.executionStartTime is None:
            print("warning: job execution start time is invalid.")
            runTime = 0
        else:
            runTime = ent.terminationTime - ent.executionStartTime
        totalRunTime = totalRunTime+runTime
        if runTime < minRunTime:
            minRunTime = runTime
        if runTime > maxRunTime:
            maxRunTime = runTime

    if workers > 0:
        avg = totalRunTime/workers
    else:
        avg = 0

    return minRunTime, maxRunTime, avg


def writeDateValues(values):
    if values is None:
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

if __name__ == "__main__":
    run()
