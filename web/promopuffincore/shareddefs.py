import string
import random # for unique key gen
import calendar
import datetime

def unix_timestamp(fromdatetime=False):
    if not fromdatetime:
        return calendar.timegm(datetime.datetime.utcnow().timetuple())
    else:
        return calendar.timegm(fromdatetime.timetuple())

def appuuid():
    """ at the moment just returns a hex from uuid but maybe replaced but riak_id """
    return str(unix_timestamp()) + '-' + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)

    