"""
This file stops circular dependencies
"""

# from auth import *
from views import *
from accounts import Accounts, Account
from campaigns import Campaigns, Campaign
from codes import Codes, Code
from validate import Validate
from redeem import Redeem

import accounts as accounts
import campaigns as campaigns


def auth_account_apikey():
    # if account_id not in accounts.accounts_data:
    #     return "Error: Account does not exists"
    return "thisandthat"


def validate_accounts(account_id):
    if account_id in accounts.accounts_data:
        return True
    return False


def init_db():
    pass


@app.before_request
def before_request():
    # init_db()
    pass

if __name__ == '__main__':
    app.run()
