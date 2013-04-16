from lsst.ctrl.stats.data.dbEntry import DbEntry

class ExecutingWorkers:

    def __init__(self, dbm):
        self.dbm = dbm
        self.firstExecutingWorker = self.getFirst()
        self.lastExecutingWorker = self.getLast()


    def getFirstExecutingWorker(self):
        return self.firstExecutingWorker

    def getLastExecutingWorker(self):
        return self.lastExecutingWorker

    def getFirst(self):
        query = "select dagNode, executionHost, slotName, UNIX_TIMESTAMP(submitTime), UNIX_TIMESTAMP(executionStartTime), UNIX_TIMESTAMP(executionStopTime), UNIX_TIMESTAMP(terminationTime)  from submissions where dagNode != 'A' and executionStartTime !='0000-00-00 00:00:00' order by executionStartTime limit 1;"

        results = self.dbm.execCommandN(query)
        dbEntry = DbEntry(results[0])

        return dbEntry


    def getLast(self):
        query = "select dagNode, executionHost, slotName, UNIX_TIMESTAMP(submitTime), UNIX_TIMESTAMP(executionStartTime), UNIX_TIMESTAMP(executionStopTime), UNIX_TIMESTAMP(terminationTime) from submissions where dagNode != 'B' and executionStartTime !='0000-00-00 00:00:00' order by executionStopTime DESC limit 1;"

        results = self.dbm.execCommandN(query)
        dbEntry = DbEntry(results[0])

        return dbEntry

        
