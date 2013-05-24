from flask import request, abort
from functools import wraps

import string
import random  # for unique key gen
import calendar
import datetime
from app import app


def unix_timestamp(fromdatetime=False):
    if not fromdatetime:
        return calendar.timegm(datetime.datetime.utcnow().timetuple())
    else:
        return calendar.timegm(fromdatetime.timetuple())


def appuuid():
    """ at the moment just returns a hex from uuid but maybe replaced but riak_id """
    return str(unix_timestamp()) + '-' + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)


def api_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get("auth", "")
        if token == app.config['PROMOPUFFIN_API_KEY']:
            pass
        else:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function


def account_api_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get("auth", "")
        if token == app.config['PROMOPUFFIN_API_KEY']:
            pass
        else:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function
