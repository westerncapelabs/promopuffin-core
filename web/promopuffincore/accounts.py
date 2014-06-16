from flask import g
from flask.ext.restful import reqparse, Resource, abort
from app import api
import shareddefs
import main

accounts_data = {}

parser = reqparse.RequestParser()
parser.add_argument('username', required=True, type=unicode)
parser.add_argument('password', required=True, type=unicode)


class Accounts(Resource):
    @shareddefs.accounts_api_token_required
    def get(self):
        """ lists all accounts """
        return get_bucket_list()

    @shareddefs.accounts_api_token_required
    def post(self):
        """ saves a new account """
        args = parser.parse_args()

        accounts_data = {
            'username': args['username'],
            'password': g.bcrypt.generate_password_hash(args['password']),
            "api_key": shareddefs.realuuid(),
        }
        # save to DB
        account_id = account_store(accounts_data)

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

### ACCOUNT LOGIN
login_parser = reqparse.RequestParser()
login_parser.add_argument('username', required=True, type=unicode, case_sensitive=True)
login_parser.add_argument('password', required=True, type=unicode, case_sensitive=True)


class AccountLogin(Resource):
    """ Login into a specific account """
    def post(self):        
        args = login_parser.parse_args()
        results = get_account(args['username'])

        for account_id in results:
            account = account_load(account_id)
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


def get_account(username):
    """ trys to find user account using username """
    query = g.rc.add(main.app.config['RIAK_BUCKET_PREFIX'] + 'accounts')
    # This gets just keys
    query.map("""
    function(v, meta, arg) {
        var data = JSON.parse(v.values[0].data);
        if(data['username'] == arg['username']){
            return [v.key];
        } else {
            return [];
        }
    }""", {"arg": {"username": username}})
    result = query.run()    
    if result is None:
        return False
    else:
        return result


def account_exists(account_id):
    """ Check account exists - return True/False """
    bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'accounts')
    t = bucket_data.get(account_id)
    if not t.exists():
        abort(404, message="Account {} doesn't exist".format(account_id))
    else:
        return True


def account_store(data, account_id=False):
    """ Stores the data object passed in to the db, retunrs new key if wasn't passed one """
    # Choose a bucket to store our data in
    bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'accounts')
    # Supply a key to store our data under
    if not account_id:
        account_id = shareddefs.appuuid()
        data_item = bucket_data.new(account_id, data=data)
    else:
        if account_exists(account_id):
            data_item = bucket_data.get(account_id)
            temp = data_item.get_data()
            temp.update(data)
            data_item.set_data(temp)
    data_item.store()
    return account_id


def account_load(account_id):
    """ Loads the account from db and returns the resulting data """
    if account_exists(account_id):
        bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'accounts')
        data_item = bucket_data.get(account_id)
        account = data_item.get_data()
        return account
    else:
        return False # account exists will handle errors


def account_delete(account_id):
    """ Removes the account from the bucket. """
    bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'accounts')
    if bucket_data.get(account_id).exists():
        bucket_data.get(account_id).delete()
        return True
    else:
        return False


def get_bucket_list():
    bucket = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'accounts')
    bucket_keys = bucket.get_keys()
    response = {}
    for key in bucket_keys:
        response[key] = bucket.get(key).get_data()
    return response

