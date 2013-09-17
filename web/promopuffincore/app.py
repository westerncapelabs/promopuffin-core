"""
App file
"""
from flask import g, Flask
from flask.ext import restful
from flaskext.bcrypt import Bcrypt
import riak


app = Flask(__name__)
app.config.from_object('promopuffincore.config.Configuration')
api = restful.Api(app)


# setup link to riak DB
def get_riak_cleint():
    g.rc = riak.RiakClient(host=app.config['RIAK_HOST'], port=app.config['RIAK_PORT'], prefix=app.config['RIAK_PREFIX'], transport_class=app.config['RIAK_TRANSPORT_CLASS'])


def get_bcrypt_ext():
    g.bcrypt = Bcrypt(app)


# set up connections etc
@app.before_request
def before_request():
    get_riak_cleint()
    # print "Riak client created..."
    get_bcrypt_ext()
