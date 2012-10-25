#!/usr/bin/env python

# 
# LSST Data Management System
# Copyright 2008, 2009, 2010 LSST Corporation.
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


# sends a logging event


import os, os.path, sys, string
import optparse
import lsst.pex.logging as log
import lsst.ctrl.events as events
from lsst.daf.base import PropertySet
from socket import gethostname

def parseArgs(argv):
    basename = os.path.basename(argv[0])

    usage = """usage: """+basename+""" --runid <runid> --workerid <workerid> --dataid <dataid> --status <status> --slot <condor_slot> --comment <comment>"""
    parser = optparse.OptionParser(usage)
    parser.add_option("-r", "--runid", action="store", default=None, dest="runId", help="run id")
    parser.add_option("-w", "--workerid", action="store", default=None, dest="workerId", help="worker id")
    parser.add_option("-d", "--dataid", action="store", default=None, dest="dataId", help="data id")
    parser.add_option("-s", "--status", action="store", default=None, dest="status", help="status")
    parser.add_option("-S", "--slot", action="store", default=None, dest="slot", help="slot")
    parser.add_option("-c", "--comment", action="store", default=None, dest="comment", help="comment")

    opts, args = parser.parse_args(argv)

    if opts.runId == None or opts.workerId == None or opts.slot == None or opts.dataId == None or opts.status == None or opts.comment == None:
        print usage
        sys.exit(10)
    return opts, args


def sendLogEvent(runid, workerid, slot, dataid, status, comment):
    host = "lsst8.ncsa.uiuc.edu"
    topic = events.EventLog.LOGGING_TOPIC
    eventSystem = events.EventSystem.getDefaultEventSystem()
    eventSystem.createTransmitter(host,topic)

    eventSystem.createReceiver(host,topic, "RUNID = '%s'" % runid)

    ps = PropertySet()
    ps.set("WORKERID", int(workerid))
    ps.set("DATAID", dataid)
    ps.set("STATUS", status)
    ps.set("SLOT", slot)
    logger = events.EventLog(runid, -1, ps, gethostname(), log.Log.INFO)

    tlog = log.Log(logger, "instrument")
    tlog.log(log.Log.INFO, comment)

    val = eventSystem.receiveEvent(topic, 100)
    assert val != None

    print val.getPropertySet().toString()

if __name__ == "__main__":

    opts, args = parseArgs(sys.argv)
    sendLogEvent(opts.runId, opts.workerId, opts.slot, opts.dataId, opts.status, opts.comment)
