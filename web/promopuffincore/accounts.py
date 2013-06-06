from flask.ext.restful import reqparse, Resource, abort
from app import api
import shareddefs

accounts_data = {}

# accounts_data_backup = {
#     "uuid_1": {
#         "username": "user1@example.com",
#         "password": "bcryptedhash",
#         "api_key": "thisandthat",
#     },
#     "uuid_2": {
#         "username": "user2@example.com",
#         "password": "bcryptedhash",
#         "api_key": "thisandthat",
#     },
#     "uuid_3": {
#         "username": "user3@example.com",
#         "password": "bcryptedhash",
#         "api_key": "thisandthat",
#     },
# }

parser = reqparse.RequestParser()
parser.add_argument('username', type=unicode)
parser.add_argument('password', type=unicode)
parser.add_argument('api_key', type=unicode)
parser.add_argument('auth', type=unicode)


def abort_account_not_found(account_id):
    if account_id not in accounts_data:
        abort(404, message="Account {} doesn't exist".format(account_id))


# returns a copy of accounts_data
def get_data(account_id):
    abort_account_not_found(account_id)
    return dict(accounts_data[account_id])


class Accounts(Resource):
    @shareddefs.accounts_api_token_required
    def get(self):
        """ lists all accounts """
        return accounts_data

    @shareddefs.accounts_api_token_required
    def post(self):
        """ saves a new account """
        args = parser.parse_args()
        account_id = 'uuid_%d' % (len(accounts_data) + 1)
        accounts_data[account_id] = {
            'username': args['username'],
            'password': args['password'],
            "api_key": args['api_key'],
        }
        return accounts_data[account_id], 201

api.add_resource(Accounts, '/accounts')


class Account(Resource):
    """ For an individual Account"""
    @shareddefs.accounts_api_token_required
    def get(self, account_id):
        """ Just one account details """
        abort_account_not_found(account_id)
        return accounts_data[account_id], 200

    @shareddefs.accounts_api_token_required
    def delete(self, account_id):
        abort_account_not_found(account_id)
        del accounts_data[account_id]
        return 'Account Successfully Deleted', 204

    @shareddefs.accounts_api_token_required
    def put(self, account_id):
        args = parser.parse_args()
        account = {
            'username': args['username'],
            'password': args['password'],
            "api_key": args['api_key'],
        }
        abort_account_not_found(account_id)
        accounts_data[account_id] = account
        return account, 201

api.add_resource(Account, '/accounts/<string:account_id>')

# class AccountSearch(Resource):
#     def get(self):
#         """take q and search accounts based on search parameters"""

# api.add_resource(Accounts, '/accounts/search')
