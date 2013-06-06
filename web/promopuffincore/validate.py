from flask.ext.restful import reqparse, Resource, abort
from app import api

import main

parser = reqparse.RequestParser()
parser.add_argument('code_id', type=unicode)
parser.add_argument('api_key', type=unicode)
parser.add_argument('code', type=unicode)
parser.add_argument('friendly_code', type=unicode)
parser.add_argument('transaction_amount', type=float, default=0)
parser.add_argument('transaction_currency', type=unicode, default="ZAR")

validate_data = {}


def abort_code_not_found(code_id):
    if code_id not in main.codes.codes_data:
        abort(404, message="Code {} doesn't exist".format(code_id))


def abort_campaign_not_found(campaign_id):
    if campaign_id not in main.campaigns.campaigns_data:
        abort(404, message="Campaign {} doesn't exist".format(campaign_id))


# TODO
def validate_data(data):
    response = {
        "valid": True,
        "value_type": "fixed",
        "value_amount": 50.00,
        "value_currency": "ZAR",
    }

    abort_code_not_found(data['code'])
    code_data = main.codes.codes_data[data['code']]

    return response


class Validate(Resource):
    """ Validates code data """
    # @shareddefs.validate_api_token_required
    def post(self):
        args = parser.parse_args()
        data = {
            'code_id': args['code_id'],
            'api_key': args['api_key'],
            'code': args['code'],
            'friendly_code': args['friendly_code'],
            'transaction_amount': args['transaction_amount'],
            'transaction_currency': args['transaction_currency'],
        }
        return validate_data(data), 201


api.add_resource(Validate, '/validate')
