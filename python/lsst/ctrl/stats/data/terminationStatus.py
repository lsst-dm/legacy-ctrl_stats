from lsst.ctrl.stats.data.dbEntry import DbEntry
from lsst.ctrl.stats.data.dbEntries import DbEntries

class TerminationStatus:

    def __init__(self, dbm):
        self.dbm = dbm;

    def getTotals(self):
        query = "select eventCodes.EventName, (select count(*) from submissions where submissions.terminationCode = eventCodes.eventCode and submissions.dagNode != 'A' and submissions.dagNode != 'B') as appears from eventCodes"
    
        results = self.dbm.execCommandN(query)

        totals = []
        for r in results:
            if r[1] > 0:
                totals.append([r[0],r[1]])
    
        return totals
