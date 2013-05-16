"""
This file stops circular dependencies
"""

# from auth import *
from views import *
from accounts import Accounts, Account
from campaigns import Campaigns, Campaign


def init_db():
    pass


@app.before_request
def before_request():
    # init_db()
    pass

if __name__ == '__main__':
    app.run()
