"""
App file
"""
from flask import g, Flask
from flask.ext import restful
from flaskext.bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_object('promopuffincore.config.Configuration')
api = restful.Api(app)


def get_bcrypt_ext():
    g.bcrypt = Bcrypt(app)


# set up connections etc
@app.before_request
def before_request():
    get_bcrypt_ext()
