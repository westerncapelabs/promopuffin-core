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


def abort_account_not_found(account_id):
    if account_id not in accounts_data:
        abort(404, message="Account {} doesn't exist".format(account_id))


# returns a copy of accounts_data
def get_data(account_id):
    abort_account_not_found(account_id)
    return dict(accounts_data[account_id])


def validate_accounts_data(args):
    errors = []
    if args['username'] is None:
        errors.append("No username specified")

    if args['password'] is None:
        errors.append("No password specified")

    if args['api_key'] is None:
        errors.append("No api_key specified")

    return errors


class Accounts(Resource):
    @shareddefs.accounts_api_token_required
    def get(self):
        """ lists all accounts """
        return accounts_data

    @shareddefs.accounts_api_token_required
    def post(self):
        """ saves a new account """
        args = parser.parse_args()

        # validate input data
        errors = validate_accounts_data(args)
        if len(errors) > 0:
            return errors, 400

        account_id = shareddefs.appuuid()
        accounts_data[account_id] = {
            'username': args['username'],
            'password': args['password'],
            "api_key": shareddefs.appuuid(),
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

        # validate input data
        errors = validate_accounts_data(args)
        if len(errors) > 0:
            return errors, 400

        abort_account_not_found(account_id)
        account = accounts_data[account_id]
        account['username'] = args['username']
        account['password'] = args['password']

        return account, 201

api.add_resource(Account, '/accounts/<string:account_id>')

# class AccountSearch(Resource):
#     def get(self):
#         """take q and search accounts based on search parameters"""

# api.add_resource(Accounts, '/accounts/search')
