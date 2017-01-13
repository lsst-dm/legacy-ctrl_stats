#
# LSST Data Management System
# Copyright 2008-2013 LSST Corporation.
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
from builtins import object


class DbEntries(object):
    """A representation of the database entries for a given run

    Parameters
    ----------
    entries: list of dbEntry
         representation of all database entries for a run
    """

    def __init__(self, entries):
        """
        Constructor
        @param entries representation of all database entries for a run
        """
        # objects representing database records
        self.entries = entries

    def getEntry(self, x):
        """
        Get a specific entry
        @param x the number of the entry in the list
        @return the x-th entry in the list
        """
        return self.entries[x]

    def getDagNode(self, dagNode):
        """
        Get an entry given a DAG node name
        @param dagNode name of the node
        @return the first entry in the list that matches dagNode
        """
        for ent in self.entries:
            if ent.dagNode == dagNode:
                return ent
        return None

    def getPreJob(self):
        """
        Get the prejob entry
        @return the prejob entry
        """
        return self.getDagNode('A')

    def getPreJobExecutionStopTime(self):
        """
        Get the execution stop time of the prejob entry
        @return the time when the prejob ended
        """
        ent = self.getDagNode('A')
        return ent.executionStopTime

    def getPostJob(self):
        """
        Get the postjob entry
        @return the postjob entry
        """
        return self.getDagNode('B')

    def getLength(self):
        """
        @return the length of the dbEntries object
        """
        return len(self.entries)

    def getFirstWorker(self):
        """
        Get the first worker job in the execution
        @return an entry representing the first worker
        """
        return self.getDagNode('A1')

    def getLastWorker(self):
        """
        Get the last worker job in the execution
        @return an entry representing the last worker
        """
        if len(self.entries) > 2:
            return self.entries[-2]
        else:
            return None

    def getPostJobSubmitTime(self):
        """
        Get the submit time of the post job, if it exists.
        @return the post job's submit time or None if no postJob exists
        """
        ent = self.getPostJob()
        if ent is None:
            return None
        return ent.submitTime
