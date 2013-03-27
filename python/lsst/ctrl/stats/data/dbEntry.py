class DbEntry:

    def __init__(self, dbList):
        self.dagNode = dbList[0]
        self.executionHost = dbList[1]
        self.slotName = dbList[2]
        self.submitTime = dbList[3]
        self.executionStartTime = dbList[4]
        self.executionStopTime = dbList[5]
