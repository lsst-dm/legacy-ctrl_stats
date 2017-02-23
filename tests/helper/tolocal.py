from dateutil import parser, tz

def tolocal(dateVal):
    dt = parser.parse(dateVal)
    dt = dt.replace(tzinfo=tz.tzlocal())
    stamp = dt.strftime('%Y-%m-%d %H:%M:%S%z')
    return stamp

