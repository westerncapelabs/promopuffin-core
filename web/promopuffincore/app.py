"""
App file
"""
from flask import Flask
from flask.ext import restful


app = Flask(__name__)
app.config.from_object('promopuffincore.config.Configuration')
api = restful.Api(app)
