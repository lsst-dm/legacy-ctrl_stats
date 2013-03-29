from lsst.ctrl.stats.data.dbEntry import DbEntry
from lsst.ctrl.stats.data.dbEntries import DbEntries

class InitialSubmissionTimes:

    def __init__(self, dbm):
        query = "select a.dagNode, a.executionHost, a.slotName, UNIX_TIMESTAMP(a.submitTime), UNIX_TIMESTAMP(a.executionStartTime), UNIX_TIMESTAMP(a.executionStopTime), UNIX_TIMESTAMP(a.terminationTime)  from submissions a inner join ( select dagNode, min(id) minID from submissions group by dagNode) b on a.dagNode = b.dagNode and a.id = b.minId order by a.submitTime, a.id;"
    
        results = dbm.execCommandN(query)
    
        ents = []
        for res in results:
            dbEnt = DbEntry(res)
            ents.append(dbEnt)

        self.entries = DbEntries(ents)
    

    def getEntries(self):
        return self.entries
