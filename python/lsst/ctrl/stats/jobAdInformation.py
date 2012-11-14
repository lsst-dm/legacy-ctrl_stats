from record import Record
class JobAdInformation(Record):
    """
    Job ad information event triggered
    Extra job ClassAd attributed are noted.  This event is written
    as a supplement to other events when the configuration paramter
    EVENT_LOG_JOB_AD_INFORMATION_ATTRS is set.
    """
    def __init__(self, year, lines):
        Record.__init__(self, year, lines)
