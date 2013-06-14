# config
import riak


class Configuration(object):
    DEBUG = True
    SECRET_KEY = 'putsomethingheresomeday'
    PROMOPUFFIN_API_KEY = 'somekey'
    CURRENCY = 'ZAR'
    SECRET_KEY = '\x8a\xa2@\xfd\xf1\xb8\x7f,\x93D\x1d\xe6\xfd\xcb\xbf?\x02z\xf8\x0e\xa7\x00\xbaA,h\xfd\xe6\x96)\xf6o\xbf\xcar|\n\x83\x1e\xbc\xa5h\x9c\xc3\x8c4b\x9eI\x878\x83\x00\x8c\xcb-\xfe\xcd\x9b\x8b\xb0\x9a\n\xf4'
    RIAK_HOST = 'localhost'
    RIAK_PORT = 8098
    # RIAK_PORT = 8087
    RIAK_PREFIX = 'riak'
    RIAK_TRANSPORT_CLASS = riak.RiakPbcTransport
    RIAK_BUCKET_PREFIX = ''


class DevelopmentConfig(object):
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'putsomethingheresomeday'
    PROMOPUFFIN_API_KEY = 'somekey'
    RIAK_HOST = 'localhost'
    RIAK_PORT = 8098
    # RIAK_PORT = 8087
    RIAK_PREFIX = 'riak'
    RIAK_TRANSPORT_CLASS = riak.RiakPbcTransport
    RIAK_BUCKET_PREFIX = 'test_'
