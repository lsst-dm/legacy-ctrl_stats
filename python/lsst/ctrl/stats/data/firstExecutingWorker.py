from lsst.ctrl.stats.data.dbEntry import DbEntry

class FirstExecutingWorker:

    def __init__(self, dbm):
        self.dbm = dbm

    def calculate(self):
        query = "select dagNode, executionHost, slotName, UNIX_TIMESTAMP(submitTime), UNIX_TIMESTAMP(executionStartTime), UNIX_TIMESTAMP(executionStopTime)  from submissions where dagNode != 'A' order by executionStartTime limit 1;"

        results = self.dbm.execCommandN(query)
        dbEntry = DbEntry(results[0])

        return dbEntry

        
