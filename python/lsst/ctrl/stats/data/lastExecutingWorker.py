from lsst.ctrl.stats.data.dbEntry import DbEntry
class LastExecutingWorker:

    def __init__(self, dbm):
        self.dbm = dbm

    def calculate(self):
        query = "select dagNode, executionHost, slotName, UNIX_TIMESTAMP(submitTime), UNIX_TIMESTAMP(executionStartTime), UNIX_TIMESTAMP(executionStopTime)  from submissions where dagNode != 'B' order by executionStopTime DESC limit 1;"

        results = self.dbm.execCommandN(query)
        dbEntry = DbEntry(results[0])

        return dbEntry

        
