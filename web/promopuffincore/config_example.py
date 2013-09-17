# config

####################
# NOTE: these settings are examples only! Make a copy with your own values for production purposes
####################

import riak


class Configuration(object):
    DEBUG = True
    SECRET_KEY = 'putsomethingheresomeday'
    PROMOPUFFIN_API_KEY = 'somekey'
    CURRENCY = 'ZAR'
    RIAK_HOST = '127.0.0.1'
    # RIAK_PORT = 8098
    RIAK_PORT = 8087
    RIAK_PREFIX = 'riak'
    RIAK_TRANSPORT_CLASS = riak.RiakPbcTransport
    RIAK_BUCKET_PREFIX = 'promopuffin_core_'
