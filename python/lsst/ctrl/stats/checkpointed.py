from record import Record
class Checkpointed(Record):
    """
    Job was checkpointed
    The job's complete state was written to a checkpoint file.  This might
    happen without the job being removed from the machine, because the
    checkpointing can happen periodically.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)

    def printAll(self):
        print "C",self.lines
