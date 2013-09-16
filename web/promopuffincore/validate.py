from flask.ext.restful import reqparse, Resource
from flask import g
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
    code_data = main.codes.code_load(data['code_id'])
    response = {
        "valid": False,
        "error": [],
    }

    # list of validation of checks
    if code_data['code'] != data['code']:
        response['error'].append("code did not match campaign code(unique system-wide)")

    if code_data['friendly_code'] != data['friendly_code']:
        response['error'].append("friendly_code did not match campaign friendly_code(unique per campaign)")

    if code_data['value_currency'] != data['transaction_currency']:
        response['error'].append("value_currency did not match campaign currency")

    if data['transaction_amount'] < code_data['minimum']:
        response['error'].append("transaction_amount was less than campaign minimum")

    account_id = main.campaigns.campaign_load(code_data['campaign_id'])['account_id']
    if data['api_key'] != main.accounts.account_load(account_id)['api_key']:
        response['error'].append("api_key did not match accounts api_key for campaign")

    # check if any errors in validation
    if len(response['error']) == 0:
        response = {
            "valid": True,
            "value_type": code_data['value_type'],
            "value_currency": code_data['value_currency'],
        }
        if code_data['value_type'] == 'fixed':
            response['value_amount'] = data['transaction_amount'] - code_data['value_amount']
        elif code_data['value_type'] == 'percentage':
            response['value_amount'] = data['transaction_amount'] * (code_data['value_amount']/100)

    return response


class Validate(Resource):
    """ Validates code data """
    def post(self):
        args = parser.parse_args()
        main.codes.code_exists(args['code_id'])
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
            return response, 400  # bad request


api.add_resource(Validate, '/validate')
