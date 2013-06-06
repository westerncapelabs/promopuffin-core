from flask.ext.restful import reqparse, Resource, abort
from app import api

import shareddefs

parser = reqparse.RequestParser()
parser.add_argument('api_key', type=unicode)
parser.add_argument('code', type=unicode)
parser.add_argument('friendly_code', type=unicode)
parser.add_argument('transaction_amount', type=float, default=0)
parser.add_argument('transaction_currency', type=unicode, default="ZAR")

redeemed_data = {}


def abort_code_not_found(code_id):
    if code_id not in redeemed_data:
        abort(404, message="Code {} doesn't exist".format(code_id))


def abort_campaign_not_found(campaign_id):
    if campaign_id not in redeemed_data:
        abort(404, message="Campaign {} doesn't exist".format(campaign_id))


# TODO still
def redeem_data(data):
    response = {
        "valid": True,
        "status": "available",
        "total": 50.00,
        "remaining": 28.00,
    }
    abort_code_not_found(data['code'])
    return response


class Redeem(Resource):
    """ Validates code data """
    # @shareddefs.api_token_required
    def post(self):
        args = parser.parse_args()
        data = {
            'api_key': args['api_key'],
            'code': args['code'],
            'friendly_code': args['friendly_code'],
            'transaction_amount': args['transaction_amount'],
            'transaction_currency': args['transaction_currency'],
        }
        return redeemed_data(data), 201


api.add_resource(Redeem, '/redeem')
