from lsst.ctrl.stats.data.dbEntry import DbEntry
from lsst.ctrl.stats.data.dbEntries import DbEntries

class SuccessTimes:

    def __init__(self, dbm):
        query = "select dagNode, executionHost, slotName, UNIX_TIMESTAMP(submitTime), UNIX_TIMESTAMP(executionStartTime), UNIX_TIMESTAMP(executionStopTime), UNIX_TIMESTAMP(terminationTime) from submissions where terminationCode='005';"
    
        results = dbm.execCommandN(query)
    
        ents = []
        for res in results:
            dbEnt = DbEntry(res)
            ents.append(dbEnt)

        self.entries = DbEntries(ents)
    

    def getEntries(self):
        return self.entries
