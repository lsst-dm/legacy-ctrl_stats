class DbEntries:

    def __init__(self, entries):
        self.entries = entries

    def getEntry(self, x):
        return self.entries[x]

    def getDagNode(self, dagNode):
        for ent in self.entries:
            if ent.dagNode == dagNode:
                return ent
        return None
    
    def getPreJob(self):
        return self.getDagNode('A')

    def getPreJobExecutionStopTime(self):
        ent = self.getDagNode('A')
        return ent.executionStopTime
    
    def getPostJob(self):
        return self.getDagNode('B')

    def getLength(self):
        return len(self.entries)

    def getFirstWorker(self):
        return self.getDagNode('A1')

    def getLastWorker(self):
        return self.entries[-2]

    def getPostJobSubmitTime(self):
        ent = self.getPostJob()
        return ent.submitTime
