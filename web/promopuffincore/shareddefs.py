from flask import g, request, abort
from functools import wraps
import main

import string
import random  # for unique key gen
import calendar
import datetime
import uuid
from app import app


def unix_timestamp(fromdatetime=False):
    if not fromdatetime:
        return calendar.timegm(datetime.datetime.utcnow().timetuple())
    else:
        return calendar.timegm(fromdatetime.timetuple())


def appuuid():
    """ at the moment just returns a hex from uuid but maybe replaced but riak_id """
    return str(unix_timestamp()) + '-' + random.choice(string.ascii_letters) + random.choice(string.ascii_letters)


def realuuid():
    return uuid.uuid4().hex


def accounts_api_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get("auth", "")
        print kwargs
        if 'account_id' in kwargs:
            main.accounts.account_exists(kwargs['account_id'])
            if token == main.accounts.accounts_data[kwargs['account_id']]["api_key"]:
                pass
            elif token == app.config['PROMOPUFFIN_API_KEY']:
                pass
            else:
                abort(401)
        elif token == app.config['PROMOPUFFIN_API_KEY']:
            pass
        else:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function


def campaigns_api_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.args.get("auth", "")
        if 'campaign_id' in kwargs:
            main.campaigns.abort_campaign_not_found(kwargs['campaign_id'])
            account_id = main.campaigns.campaigns_data[kwargs['campaign_id']]['account_id']
            main.accounts.abort_account_not_found(account_id)
            if token == main.accounts.accounts_data[account_id]['api_key']:
                pass
            elif token == app.config['PROMOPUFFIN_API_KEY']:
                pass
            else:
                abort(401)
        elif token == app.config['PROMOPUFFIN_API_KEY']:
            pass
        else:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function
