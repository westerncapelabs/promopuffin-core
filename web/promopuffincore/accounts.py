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

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', required=True, type=unicode, case_sensitive=True)
login_parser.add_argument('password', required=True, type=unicode, case_sensitive=True)
login_parser.add_argument('account_id', required=True, type=unicode, case_sensitive=True)


class Accounts(Resource):
    @shareddefs.accounts_api_token_required
    def get(self):
        """ lists all accounts """
        return get_bucket_list()

    @shareddefs.accounts_api_token_required
    def post(self):
        """ saves a new account """
        args = parser.parse_args()

        account_id = shareddefs.appuuid()
        accounts_data = {
            'username': args['username'],
            'password': g.bcrypt.generate_password_hash(args['password']),
            "api_key": shareddefs.realuuid(),
        }
        # save to DB
        account_store(accounts_data, account_id)

        response = {
            "account_id": account_id,
            "username": accounts_data['username'],
            "api_key": accounts_data['api_key'],
        }
        return response, 201

api.add_resource(Accounts, '/accounts')


class Account(Resource):
    """ For an individual Account"""
    @shareddefs.accounts_api_token_required
    def get(self, account_id):
        """ Just one account details """
        account_exists(account_id)
        return account_load(account_id), 200

    @shareddefs.accounts_api_token_required
    def delete(self, account_id):
        account_exists(account_id)
        account_delete(account_id)
        return 'Account Successfully Deleted', 204

    @shareddefs.accounts_api_token_required
    def put(self, account_id):
        args = parser.parse_args()

        account_exists(account_id)
        account_data = {
            'username': args['username'],
            'password': g.bcrypt.generate_password_hash(args['password']),
        }

        # save to DB
        item_id = account_store(account_data, account_id)
        account = account_load(item_id)

        response = {
            "account_id": item_id,
            "username": account['username'],
            "api_key": account['api_key'],
        }

        return response, 201

api.add_resource(Account, '/accounts/<string:account_id>')


class AccountLogin(Resource):
    """ Login into a specific account """
    def post(self):
        args = login_parser.parse_args()
        account_exists(args['account_id'])
        account = account_load(args['account_id'])

        if account['username'] == args['username']:
            if g.bcrypt.check_password_hash(account['password'], args['password']):
                return account['api_key'], 201

        return "Unauthorized: Incorrect username and password match", 401

api.add_resource(AccountLogin, '/accounts/login')

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
    """ Removes the product from the bucket. """
    bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'accounts')
    if bucket_data.get(account_id).exists():
        bucket_data.get(account_id).delete()
        return True
    else:
        return False


def get_bucket_list():
    return g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'accounts').get_keys()
