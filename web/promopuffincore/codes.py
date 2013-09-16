from flask import g
from flask.ext.restful import reqparse, Resource, abort
from app import api

import main
import shareddefs

parser = reqparse.RequestParser()
parser.add_argument('code', required=True, type=unicode, case_sensitive=True)
parser.add_argument('friendly_code', required=True, type=unicode, case_sensitive=True)
parser.add_argument('description', required=True, type=unicode)
parser.add_argument('status', type=unicode, default="unused")
parser.add_argument('value_type', required=True, type=unicode)
parser.add_argument('value_amount', required=True, type=float, default=0)
parser.add_argument('value_currency', type=unicode, default=main.app.config['CURRENCY'])
parser.add_argument('minimum', required=True, type=float, default=0)
parser.add_argument('total', required=True, type=int, default=0)
parser.add_argument('history_msg', type=unicode)
parser.add_argument('remaining', required=True, type=int, default=0)


def find_all_campaign_codes(campaign_id):
    temp_data = {}
    codes_data = get_bucket_list()
    for code in codes_data.itervalues():
        if campaign_id == code['campaign_id']:
            temp_data[len(codes_data) + 1] = dict(code)

    return temp_data


def set_data(code_id, data):
    code_exists(code_id)
    code_store(data, code_id)
    return True


def validate_new_codes_data(args):
    errors = []
    if args['value_amount'] < 0:
        errors.append("value_amount is less than 0")

    if args['minimum'] < 0:
        errors.append("minimum is less than 0")

    if args['total'] < 0:
        errors.append("total is less than 0")

    if args['remaining'] > args['total']:
        errors.append("Number of remaining is greater than total")

    if args['remaining'] < 0:
        errors.append("remaining is less than 0")

    return errors


def append_to_history(code_id, msg):
    """ Appends something to the "history" element of an existing event """
    bucket = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'codes')
    if code_exists(code_id):
        code = bucket.get(code_id)  # always run product_exists first
        details = code.get_data()  # retrieve the data
        if "history" in details:
            details["history"].update({shareddefs.unix_timestamp(): msg})
        else:
            details.update({"history": {shareddefs.unix_timestamp(): msg}})
        code.set_data(details)
        code.store()
        return True
    else:
        return False


class Codes(Resource):
    @shareddefs.campaigns_api_token_required
    def get(self, campaign_id):
        """ lists all codes """
        return find_all_campaign_codes(campaign_id)

    @shareddefs.campaigns_api_token_required
    def post(self, campaign_id):
        """ saves a new code """
        args = parser.parse_args()

        # validate input data
        errors = validate_new_codes_data(args)
        if len(errors) > 0:
            return errors, 400

        code_data = {
            'campaign_id': campaign_id,
            'code': args['code'],
            'friendly_code': args['friendly_code'],
            "description": args['description'],
            "status": args['status'],
            "value_type": args['value_type'],
            "value_amount": args['value_amount'],
            "value_currency": args['value_currency'],
            "minimum": args['minimum'],
            "total": args['total'],
            "history_msg": [],
            "remaining": args['remaining'],
        }
        # save to DB
        code_id = code_store(code_data)

        return code_data, 201

api.add_resource(Codes, '/campaigns/<string:campaign_id>/codes')


class Code(Resource):
    """ Individual Code """
    @shareddefs.campaigns_api_token_required
    def get(self, campaign_id, code_id):
        code_exists(code_id)
        return code_load(code_id), 200

    @shareddefs.campaigns_api_token_required
    def put(self, campaign_id, code_id):
        args = parser.parse_args()

        # validate input data
        errors = validate_new_codes_data(args)
        if len(errors) > 0:
            return errors, 400

        code_exists(code_id)
        code_data = {
            'campaign_id': campaign_id,
            'code': args['code'],
            'friendly_code': args['friendly_code'],
            "description": args['description'],
            "status": args['status'],
            "value_type": args['value_type'],
            "value_amount": args['value_amount'],
            "value_currency": args['value_currency'],
            "minimum": args['minimum'],
            "total": args['total'],
            "remaining": args['remaining'],
            "history_msg": [],
        }
        if "history_msg" in args:
            code_data['history_msg'].append(args['history_msg'])
        else:
            code_data['history_msg'].append("Updated: " + unicode(shareddefs.unix_timestamp()))

        # save to DB
        code_store(code_data, code_id)

        return code_data, 201

    @shareddefs.campaigns_api_token_required
    def delete(self, campaign_id, code_id):
        code_exists(code_id)
        code_delete(code_id)
        return 'Code Successfully Deleted', 204

api.add_resource(Code, '/campaigns/<string:campaign_id>/codes/<string:code_id>')


#####################
# DB Helper Functions
#####################


def code_exists(code_id):
    """ Check code exists - return True/False """
    bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'codes')
    if code_id is None:
        abort(404, message="Code {} doesn't exist".format(code_id))
    # print(code_id)
    if not bucket_data.get(code_id).exists():
        abort(404, message="Code {} doesn't exist".format(code_id))
    else:
        return True


def code_store(data, code_id=False):
    """ Stores the data object passed in to the db, returns new key if wasn't passed one """
    # Choose a bucket to store our data in
    bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'codes')
    # Supply a key to store our data under
    if not code_id:
        code_id = shareddefs.appuuid()
        data_item = bucket_data.new(code_id, data=data)
    else:
        if code_exists(code_id):
            data_item = bucket_data.get(code_id)
            temp = data_item.get_data()
            temp.update(data)
            data_item.set_data(temp) # update data record
    data_item.store()
    return code_id


def code_load(code_id):
    """ Loads the code from db and returns the resulting data """
    if code_exists(code_id):
        bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'codes')
        data_item = bucket_data.get(code_id)
        return data_item.get_data()
    else:
        pass  # code_exists will handle errors for us


def code_delete(code_id):
    """ Removes the code from the bucket. """
    bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'codes')
    if bucket_data.get(code_id).exists():
        bucket_data.get(code_id).delete()
        return True
    else:
        return False


def get_bucket_list():
    bucket = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'codes')
    bucket_keys = bucket.get_keys()
    response = {}
    for key in bucket_keys:
        response[key] = bucket.get(key).get_data()
    return response


def clear_bucket():
    bucket = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'codes')
    bucket_keys = bucket.get_keys()
    for key in bucket_keys:
        bucket.get(key).delete()
    return "Deleted all values from accounts bucket..."
