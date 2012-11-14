from record import Record
class AttributeUpdate(Record):
    """
    Attribute update
    Undefined by Condor documentation
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
