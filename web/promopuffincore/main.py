"""
This file stops circular dependencies
"""

# from auth import *
from views import *
# from accounts import Accounts, Account
import accounts
from campaigns import Campaigns, Campaign
from codes import Codes


def init_db():
    accounts.accounts_data = accounts.accounts_data_backup.copy()


@app.before_request
def before_request():
    # init_db()
    pass

if __name__ == '__main__':
    app.run()
