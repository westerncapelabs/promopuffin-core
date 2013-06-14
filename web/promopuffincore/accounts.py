from flask import g
from flask.ext.restful import reqparse, Resource, abort
from app import api
import shareddefs
import main

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
parser.add_argument('username', required=True, type=unicode)
parser.add_argument('password', required=True, type=unicode)

class Accounts(Resource):
    @shareddefs.accounts_api_token_required
    def get(self):
        """ lists all accounts """
        return shareddefs.get_bucket_list('accounts')

    @shareddefs.accounts_api_token_required
    def post(self):
        """ saves a new account """
        args = parser.parse_args()

        account_id = shareddefs.appuuid()
        accounts_data[account_id] = {
            'username': args['username'],
            'password': g.bcrypt.generate_password_hash(args['password']),
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

        abort_account_not_found(account_id)
        account = accounts_data[account_id]
        account['username'] = args['username']
        account['password'] = g.bcrypt.generate_password_hash(args['password'])

        accounts_data[account_id] = account

        return account, 201

api.add_resource(Account, '/accounts/<string:account_id>')

# class AccountSearch(Resource):
#     def get(self):
#         """take q and search accounts based on search parameters"""

# api.add_resource(Accounts, '/accounts/search')

#####################
# DB Helper Functions
#####################


def account_exists(account_id):
    """ Check product exists - return True/False """
    bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'accounts')
    if not bucket_data.get(account_id).exists():
        abort(404, message="Account {} doesn't exist".format(account_id))


def account_store(data, account_id=False):
    """ Stores the data object passed in to the db, retunrs new key if wasn't passed one """
    # Choose a bucket to store our data in
    bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'accounts')
    # value.update({"lastUpdated": unix_timestamp()})
    # Supply a key to store our data under
    if not account_id:
        account_id = shareddefs.appuuid()
        data_item = bucket_data.new(account_id, data=data)
    else:
        data_item = bucket_data.get(account_id)
        data_item.set_data(data)
    data_item.store()
    return account_id


def account_load(account_id):
    """ Loads the product from db and returns the resulting object """
    bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'accounts')
    product = bucket_data.get(account_id)  # always run product_exists first
    return product.get_data()


def account_delete(account_id):
    """ Removes the product from the bucket. Optionally remove variants and images too. Bad to leave them around. """
    bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'accounts')
    if bucket_data.get(account_id).exists():
        bucket_data.get(account_id).delete()
        return True
    else:
        return False


def get_bucket_list():
    return g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'accounts').get_keys()
