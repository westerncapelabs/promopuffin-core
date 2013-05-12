"""
views imports app, auth, and models, but none of these import views
"""
from flask import render_template

from app import app


@app.route('/')
def homepage():
    return "homepage"


@app.route('/heartbeat')
def heartbeat():
    return "Hello World!"
