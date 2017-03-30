import datetime
from dateutil import parser, tz


def utcTzLocal(dateVal):
    dt = parser.parse(dateVal)
    utc = dt.replace(tzinfo=tz.tzutc())
    local = utc.astimezone(tz.tzlocal())
    stamp = local.strftime('%Y-%m-%d %H:%M:%S%z')
    return stamp


def addTzLocal(dateVal):
    dt = parser.parse(dateVal)
    dt = dt.replace(tzinfo=tz.tzlocal())
    stamp = dt.strftime('%Y-%m-%d %H:%M:%S%z')
    return stamp


def assertTimeEqual(utctimestamp, dateString):
    assertEqual(utcTzLocal(utctimestamp), addTzLocal(dateString))


if __name__ == '__main__':
    print(utcTzLocal(1476752397))
