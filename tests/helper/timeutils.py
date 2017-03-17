import datetime
from dateutil import parser, tz


def utc_tzlocal(dateVal):
    dt = parser.parse(dateVal)
    utc = dt.replace(tzinfo=tz.tzutc())
    local = utc.astimezone(tz.tzlocal())
    stamp = local.strftime('%Y-%m-%d %H:%M:%S%z')
    return stamp


def add_tzlocal(dateVal):
    dt = parser.parse(dateVal)
    dt = dt.replace(tzinfo=tz.tzlocal())
    stamp = dt.strftime('%Y-%m-%d %H:%M:%S%z')
    return stamp


def assertTimeEqual(utctimestamp, dateString):
    assertEqual(utc_tzlocal(utctimestamp), add_tzlocal(dateString))


if __name__ == '__main__':
    print(utc_tzlocal(1476752397))
