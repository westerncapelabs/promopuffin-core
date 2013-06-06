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


def validate_data(data):
    main.codes.abort_code_not_found(data['code_id'])
    code_data = main.codes.codes_data[data['code_id']]
    response = {
        "valid": False,
        "value_type": code_data['value_type'],
        "value_amount": code_data['value_amount'],
        "value_currency": code_data['value_currency'],
    }

    if code_data['code'] != data['code'] or code_data['friendly_code'] != data['friendly_code'] or code_data['value_currency'] != data['transaction_currency']:
        return response
    if data['transaction_amount'] < code_data['minimum']:
        return response

    main.campaigns.abort_campaign_not_found(code_data['campaign_id'])
    account_id = main.campaigns.campaigns_data[code_data['campaign_id']]['account_id']
    main.accounts.abort_account_not_found(account_id)
    if data['api_key'] != main.accounts.accounts_data[account_id]['api_key']:
        return response

    response['valid'] = True
    return response


class Validate(Resource):
    """ Validates code data """
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
        response = validate_data(data)
        if response['valid'] is True:
            return response, 201
        else:
            return response, 404


api.add_resource(Validate, '/validate')
