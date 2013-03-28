from lsst.ctrl.stats.data.dbEntry import DbEntry
from lsst.ctrl.stats.data.dbEntries import DbEntries

class WorkerTotal:

    def __init__(self, dbm):
        self.dbm = dbm;

    def getTotal(self, tableName):
        query = "select  count(dagNode) from %s where dagNode != 'A' and dagNode != 'B'" % tableName
    
        results = self.dbm.execCommand1(query)
    
        return results
