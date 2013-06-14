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
        if 'account_id' in kwargs:
            main.accounts.abort_account_not_found(kwargs['account_id'])
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

###################################
# DB related helper functions {TODO}
###################################


def item_exists(bucket_name, key):
    """ Check product exists - return True/False """
    bucket_data = g.rc.bucket(app.config['RIAK_BUCKET_PREFIX'] + bucket_name)
    return bucket_data.get(key).exists()


def db_store(bucket_name, value, key=False):
    """ Stores the data object passed in to the db, retunrs new key if wasn't passed one """
    # Choose a bucket to store our data in
    bucket_data = g.rc.bucket(app.config['RIAK_BUCKET_PREFIX'] + bucket_name)
    value.update({"lastUpdated": unix_timestamp()})
    # Supply a key to store our data under
    if not key:
        key = appuuid()
        data_item = bucket_data.new(key, data=value)
    else:
        data_item = bucket_data.get(key)
        data_item.set_data(value)
    data_item.store()
    return key


def history_append(key, msg):
    """ Appends something to the "history" element of an existing event """
    products = g.rc.bucket(app.config['RIAK_BUCKET_PREFIX'] + 'products')
    if item_exists(key):
        product = products.get(key)  # always run product_exists first
        details = product.get_data()  # retrieve the data
        if "history" in details:
            details["history"].update({unix_timestamp(): msg})
        else:
            details.update({"history": {unix_timestamp(): msg}})
        db_store(details, key)
        return True
    else:
        return False


def bucket_item_load(bucket_name, key):
    """ Loads the product from db and returns the resulting object """
    bucket_data = g.rc.bucket(app.config['RIAK_BUCKET_PREFIX'] + bucket_name)
    product = bucket_data.get(key)  # always run product_exists first
    details = product.get_data()  # What???
    return True


def bucket_item_delete(bucket_name, key, removevariants=False, removeimages=False):
    """ Removes the product from the bucket. Optionally remove variants and images too. Bad to leave them around. """
    bucket_data = g.rc.bucket(app.config['RIAK_BUCKET_PREFIX'] + bucket_name)
    if bucket_data.get(key).exists():
        bucket_data.get(key).delete()
        return True
    else:
        return False


def get_bucket_list(bucket_name):
    bucket_data = g.rc.bucket(
        app.config['RIAK_BUCKET_PREFIX'] + bucket_name).get_keys()
    return bucket_data
