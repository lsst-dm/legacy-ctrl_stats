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
from __future__ import print_function
from builtins import str
from builtins import object
from datetime import datetime, timedelta
from dateutil import tz
import sys
from lsst.ctrl.stats.data.workerTotal import WorkerTotal
from lsst.ctrl.stats.data.submissionTimes import SubmissionTimes
from lsst.ctrl.stats.data.successTimes import SuccessTimes
from lsst.ctrl.stats.data.executionsPerSlot import ExecutionsPerSlot
from lsst.ctrl.stats.data.newJobStart import NewJobStart
from lsst.ctrl.stats.data.terminationStatus import TerminationStatus
from lsst.ctrl.stats.data.executingWorkers import ExecutingWorkers
from lsst.ctrl.stats.data.slotUtilization import SlotUtilization


class Report(object):
    """Report various statistics
    """

    def __init__(self, dbm, outputLocalTime=False):
        self.dbm = dbm
        self.outputLocalTime = outputLocalTime

        submitTimes = SubmissionTimes(self.dbm)
        self.entries = submitTimes.getEntries()

        firstWorker = self.entries.getFirstWorker()
        if firstWorker is None:
            raise Exception("No jobs run")

        self.executingWorkers = ExecutingWorkers(self.dbm)

    def slotUtilization(self):
        """Print number of HTCondor slots used during execution
        """
        su = SlotUtilization(self.dbm)
        slots = su.slotsUtilized()

        initialFirstWorker = self.entries.getFirstWorker()

        print("Maximum number of slots used: %d" % slots)
        stamp = self.timeStamp(su.getLastTime() - su.getFirstTime())
        print("Time until %d slots are used at least once: %s" % (slots, stamp))
        stamp = self.timeStamp(su.getLastTime()-initialFirstWorker.submitTime)
        print("First job submit to %d slots used at least once: %s" % (slots,
              stamp))
        print()

    def slottedJobCount(self):
        """Calculate the number of jobs that executed in HTCondor slots
        """
        jobs = 0
        for i in range(self.entries.getLength()):
            ent = self.entries.getEntry(i)
            if ent.slotName == '':
                continue
            jobs = jobs + 1
        return jobs

    def initialJobs(self):
        """Print the number of submitted, non-slot scheduled, slot
        scheduled jobs, and statistics about initial job submission times.
        """
        count = self.entries.getLength()
        slottedJobs = self.slottedJobCount()

        firstWorker = self.entries.getFirstWorker()
        node = firstWorker.dagNode
        submitTime = self.dateTime(firstWorker.submitTime)

        lastWorker = self.entries.getLastWorker()
        submissionDuration = lastWorker.submitTime-firstWorker.submitTime

        print("Total non-execution node jobs: %d" % (count-slottedJobs))
        print("Total execution node jobs: %d" % slottedJobs)
        print("Total submits: %d" % count)
        if submissionDuration > 0:
            print("Mean initial job submissions per second: %d" %
                  (count/submissionDuration))
        else:
            print("Initial jobs all submitted at the same time")
        print()

        print("Initial submission - first job %s submitted at %s" % (node,
              submitTime))

        node = lastWorker.dagNode
        submitTime = self.dateTime(lastWorker.submitTime)
        print("Initial submission - last job %s submitted at %s" % (node,
              submitTime))

        print("Initial submission - first job to last job submitted: %s" %
              self.timeStamp(submissionDuration))
        print()

    def _jobTiming(self, worker, prefix):
        """Print timing information about a worker
        @param worker: the record containing worker information
        @param prefix: string prefix to prepend to output
        """
        dagNode = worker.dagNode
        startTime = worker.executionStartTime
        stopTime = worker.executionStopTime
        if startTime is None:
            print("warning: %s job has not set start time" % prefix)
        if stopTime is None:
            print("warning: %s job has not set stop time")
        if startTime is not None and stopTime is not None:
            print("%s job %s started at %s" % (prefix, dagNode,
                  self.dateTime(startTime)))
            print("%s job %s stopped at %s" % (prefix, dagNode,
                  self.dateTime(stopTime)))
            print("%s job %s run duration %s" % (prefix, dagNode,
                  self.timeStamp(stopTime-startTime)))
        print()

    def firstExecutingJob(self):
        """ Print the timing information about the first job that executed
        in a slot
        """
        worker = self.executingWorkers.getFirstExecutingWorker()
        self._jobTiming(worker, "First execution node")

    def firstSubmittedJob(self):
        """ Print the timing information about the first job that was
        submitted to the HTCondor queue
        """
        worker = self.entries.getFirstWorker()
        self._jobTiming(worker, "First non-execution node ")

    def lastSubmittedJob(self):
        """ Print the timing information about the last job that was
        submitted to the HTCondor queue
        """
        worker = self.entries.getLastWorker()
        self._jobTiming(worker, "Last non-execution node")

    def lastExecutingJob(self):
        """ Print the timing information about the last job that executed
        in a slot
        """
        worker = self.executingWorkers.getLastExecutingWorker()
        self._jobTiming(worker, "Last execution node")

    def jobOverall(self):
        """Print how long it took from first job submission to last
        executing job submission and first executing job start time
        to the last executing job completion
        """
        # job overall
        lastWorker = self.entries.getLastWorker()
        firstWorker = self.entries.getFirstWorker()
        submitDuration = lastWorker.submitTime - firstWorker.submitTime
        print("First executing job submit until last executing job submit: %s"
              % self.timeStamp(submitDuration))

        first = self.executingWorkers.getFirstExecutingWorker()
        last = self.executingWorkers.getLastExecutingWorker()
        jobRunTime = last.executionStopTime - first.executionStartTime
        print("First executing job started to last executing job finished: %s"
              % (self.timeStamp(jobRunTime)))
        print()

    def jobRunTimes(self, entries):
        """Compute job run times
        @param entries: a list of job entries to use to calculate times.
        @return: minimum run time, maximum run time, average run time
        """
        jobs = 0
        totalRunTime = 0
        maxRunTime = - sys.maxsize - 1  # max negative
        minRunTime = sys.maxsize  # max positive
        length = entries.getLength()
        for i in range(length):
            ent = entries.getEntry(i)
            if ent.slotName == '':
                continue
            if ent.executionStartTime == 0:
                continue
            jobs = jobs + 1
            if ent.terminationTime is None:
                runTime = 0
                continue
            elif ent.executionStartTime is None:
                runTime = 0
                continue
            else:
                runTime = ent.terminationTime - ent.executionStartTime
            totalRunTime = totalRunTime+runTime
            if runTime < minRunTime:
                minRunTime = runTime
            if runTime > maxRunTime:
                maxRunTime = runTime

        if jobs > 0:
            avg = totalRunTime/jobs
        else:
            avg = 0

        return minRunTime, maxRunTime, avg

    def successfulRunTimes(self):
        """Print information about successful jobs
        """
        successTimes = SuccessTimes(self.dbm)
        successEntries = successTimes.getEntries()

        minRunTime, maxRunTime, avg = self.jobRunTimes(successEntries)
        print("Minimum successful job run time: %s" %
              self.timeStamp(minRunTime))
        print("Maximum successful job run time: %s" %
              self.timeStamp(maxRunTime))
        print("Mean successful job run time: %s" % self.timeStamp(avg))
        print()

    def allRunTimes(self):
        """Print minimum, maximum and mean job run times
        """
        minRunTime, maxRunTime, avg = self.jobRunTimes(self.entries)
        print("Minimum submitted job run time: %s" % self.timeStamp(minRunTime))
        print("Maximum submitted job run time: %s" % self.timeStamp(maxRunTime))
        print("Mean submitted job run time: %s" % self.timeStamp(avg))
        print()

    def executionsPerSlot(self):
        """Print minimum, maximum and mean executions per HTCondor slot
        """
        executionsPerSlot = ExecutionsPerSlot(self.dbm)
        avg = executionsPerSlot.average()
        minVal = executionsPerSlot.min()
        maxVal = executionsPerSlot.max()
        print("Minimum executions per slot: %d" % minVal)
        print("Maximum executions per slot: %d" % maxVal)
        print("Mean executions per slot: %d" % avg)
        print()

    def totals(self):
        """Print the totals of job submissions, executions and overall
        final job statuses
        """
        # totals

        newJobStart = NewJobStart(self.dbm)
        totals = newJobStart.calculate()

        workers = WorkerTotal(self.dbm)
        print("Total execution node job submissions: %d" %
              workers.getTotal("submissions"))

        print("Total execution node jobs executed: %d" %
              workers.getTotal("totals"))
        print()

        print("Termination Status:")
        termStatus = TerminationStatus(self.dbm)
        totals = termStatus.getTotals()
        for t in totals:
            print("%s: %s" % (t[0], t[1]))

    def executionSwitchover(self):
        """Print timing information about how quickly new jobs are scheduled
        to slots once jobs complete
        """
        newJobStart = NewJobStart(self.dbm)
        totals = newJobStart.calculate()

        print("Time from the end of one worker until the next worker starts")
        totalStarts = 0
        totalMinutes = 0
        for key, value in totals.items():
            if key == -1:
                print("Single worker started: %d worker%s total" %
                      (value, 's' if value > 1 else ''))
            else:
                pS = 's' if key > 1 else ''
                pW = 's' if value > 1 else ''
                print("%d second%s until next worker ", key, pS, end='')
                print("started: %d worker%s total" % (value, pW))
                totalMinutes = totalMinutes + key*value
                totalStarts = totalStarts + value
        if totalStarts == 0:
            print("No workers scheduled for more than one slot")
        else:
            print("Mean time to next worker start: %.2f seconds" %
                  (totalMinutes/totalStarts))

        print()

    def dateTime(self, val):
        """Converts seconds into a formatted date string, with offset
        @param val: seconds, in UTC time, since epoch
        @return: a formatted date string
        """
        if val is None:
            timeVal = 0
        else:
            timeVal = val
        dt = datetime.fromtimestamp(timeVal)
        utc = dt.replace(tzinfo=tz.tzutc())
        if self.outputLocalTime:
            local = utc.astimezone(tz.tzlocal())
            return local.strftime('%Y-%m-%d %H:%M:%S%z')
        else:
            return utc.strftime('%Y-%m-%d %H:%M:%S%z')

    def timeStamp(self, val):
        """Converts seconds into a formated time string
        @param val: seconds, in UTC, since epoch
        @return: a formatted time string
        """
        return str(timedelta(seconds=val))

    def writePerTimeIntervals(self, values):
        """Print pairs of date and entries per interval
        @param values: seconds and "enteries per interval" list
        """
        if values is None:
            return
        for j in range(len(values)):
            val = values[j]
            length = len(val)
            for i in range(length):
                if (i > 0):
                    sys.stdout.write(", %s" % val[i])
                elif i == 0:
                    sys.stdout.write("%s" % self.dateTime(val[0]))
            sys.stdout.write("\n")
        return
