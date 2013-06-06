from flask.ext.restful import reqparse, Resource, abort
from app import api

import shareddefs

codes_data = {}

parser = reqparse.RequestParser()
parser.add_argument('code', type=unicode)
parser.add_argument('friendly_code', type=unicode)
parser.add_argument('type', type=unicode)
parser.add_argument('description', type=unicode)
parser.add_argument('status', type=unicode, default="unused")
parser.add_argument('value_type', type=unicode)
parser.add_argument('value_amount', type=float, default=0)
parser.add_argument('value_currency', type=unicode, default="ZAR")
parser.add_argument('minimum', type=float, default=0)
parser.add_argument('minimum_currency', type=unicode, default="ZAR")
parser.add_argument('total', type=float, default=0)
parser.add_argument('history', type=unicode)
parser.add_argument('remaining', type=float, default=0)


def abort_code_not_found(code_id):
    if code_id not in codes_data:
        abort(404, message="Code {} doesn't exist".format(code_id))


def find_all_campaign_codes(campaign_id):
    temp_data = {}
    for code in codes_data.itervalues():
        if campaign_id == code['campaign_id']:
            temp_data[len(codes_data) + 1] = dict(code)

    return temp_data


# returns a copy of codes_data
def get_data(code_id):
    abort_code_not_found(code_id)
    return dict(codes_data[code_id])


def set_data(code_id, data):
    abort_code_not_found(code_id)
    codes_data[code_id] = data


class Codes(Resource):
    @shareddefs.campaigns_api_token_required
    def get(self, campaign_id):
        """ lists all codes """
        return find_all_campaign_codes(campaign_id)

    @shareddefs.campaigns_api_token_required
    def post(self, campaign_id):
        """ saves a new code """
        args = parser.parse_args()
        code_id = 'uuid_%d' % (len(codes_data) + 1)
        # code_id = appuuid()
        codes_data[code_id] = {
            'campaign_id': campaign_id,
            'code': args['code'],
            'friendly_code': args['friendly_code'],
            "type": args['type'],
            "description": args['description'],
            "status": args['status'],
            "value_type": args['value_type'],
            "value_amount": args['value_amount'],
            "value_currency": args['value_currency'],
            "minimum": args['minimum'],
            "minimum_currency": args['minimum_currency'],
            "total": args['total'],
            "history": [],
            "remaining": args['remaining'],
        }
        return codes_data[code_id], 201

api.add_resource(Codes, '/campaigns/<string:campaign_id>/codes')


class Code(Resource):
    """ Individual Code """
    @shareddefs.campaigns_api_token_required
    def get(self, campaign_id, code_id):
        abort_code_not_found(code_id)
        return codes_data[code_id], 200

    @shareddefs.campaigns_api_token_required
    def put(self, campaign_id, code_id):
        args = parser.parse_args()
        code = {
            'code': args['code'],
            'friendly_code': args['friendly_code'],
            "type": args['type'],
            "description": args['description'],
            "status": args['status'],
            "value_type": args['value_type'],
            "value_amount": args['value_amount'],
            "value_currency": args['value_currency'],
            "minimum": args['minimum'],
            "minimum_currency": args['minimum_currency'],
            "total": args['total'],
            "history": args['history'],
            "remaining": args['remaining'],
        }
        abort_code_not_found(code_id)
        codes_data[code_id] = code
        return code, 201

    @shareddefs.campaigns_api_token_required
    def delete(self, campaign_id, code_id):
        abort_code_not_found(code_id)
        del codes_data[code_id]
        return 'Code Successfully Deleted', 204

api.add_resource(Code, '/campaigns/<string:campaign_id>/codes/<string:code_id>')
