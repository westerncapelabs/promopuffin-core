from flask.ext.restful import reqparse, Resource, abort
from app import api


accounts_data = {}

parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('password', type=str)
parser.add_argument('key', type=str)


def abort_account_not_found(account_id):
    if account_id not in accounts_data:
        abort(404, message="Account {} doesn't exist".format(account_id))


class Accounts(Resource):
    def get(self):
        """ lists all accounts """
        return accounts_data

    def post(self):
        """ saves a new account """
        args = parser.parse_args()
        account_id = 'uuid_%d' % (len(accounts_data) + 1)
        accounts_data[account_id] = {
            'username': args['username'],
            'password': args['password'],
            "key": args['key'],
        }
        return accounts_data[account_id], 201

api.add_resource(Accounts, '/accounts')


class Account(Resource):
    """ For an individual Account"""
    def get(self, account_id):
        """ Just one account details """
        abort_account_not_found(account_id)
        return accounts_data[account_id], 200

    def delete(self, account_id):
        abort_account_not_found(account_id)
        del accounts_data[account_id]
        return '', 204

    def put(self, account_id):
        args = parser.parse_args()
        account = {
            'username': args['username'],
            'password': args['password'],
            "key": args['key'],
        }
        abort_account_not_found(account_id)
        accounts_data[account_id] = account
        return account, 201

api.add_resource(Account, '/accounts/<string:account_id>')

# class AccountSearch(Resource):
#     def get(self):
#         """take q and search accounts based on search parameters"""
        

# api.add_resource(Accounts, '/accounts/search')