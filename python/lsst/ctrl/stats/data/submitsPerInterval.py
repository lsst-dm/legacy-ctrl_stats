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
import datetime

class SubmitsPerInterval:
    """
    Representation of how how many submissions happen per interval, in seconds
    """

    def __init__(self, dbm, interval):
        """
        Constructor
        @param dbm  database object used to query
        @param interval length of interval we're interested in, in seconds
        """
        ## database object used to query
        self.dbm = dbm

        query = "select UNIX_TIMESTAMP(submitTime), count(*) as count from submissions where dagNode !='A' and dagNode != 'B' group by submitTime;"

        results = self.dbm.execCommandN(query)
        startTime = results[0][0]
        count = results[0][1]

        ## submit pairs for a given interval
        self.values = []
        # cycle through the seconds, counting the number of cores being used
        # during each interval
        last = startTime
        submits = 0
        for data in results:
            dataStartTime = data[0]
            dataSubmits = data[1]
            if dataStartTime - last < interval:
                d = datetime.datetime.fromtimestamp(dataStartTime).strftime('%Y-%m-%d %H:%M:%S')
                submits = submits + dataSubmits
            else:
                self.values.append([last,submits])
                last = dataStartTime
                submits = dataSubmits
            
        self.values.append([last,submits])
        

    def getValues(self):
        """
        @return list of submit pairs for a given interval
        """
        return self.values
