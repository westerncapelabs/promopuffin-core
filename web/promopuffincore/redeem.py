from flask.ext.restful import reqparse, Resource
from app import api

import main
import shareddefs

parser = reqparse.RequestParser()
parser.add_argument('code_id', type=unicode)
parser.add_argument('api_key', type=unicode)
parser.add_argument('code', type=unicode)
parser.add_argument('friendly_code', type=unicode)
parser.add_argument('transaction_amount', type=float, default=0)
parser.add_argument('transaction_currency', type=unicode, default="ZAR")


def redeem_data(data, campaign_id):
    response = {
        "redeemed": False,
        "error": [],
    }

    # list of validation checks
    code_data = main.codes.get_data(data['code_id'])
    if code_data['remaining'] < 1:
        response['error'].append("no more redeem codes available")

    if code_data['status'] is not "available":
        response['error'].append("campaign is "+code_data['status'])

    if code_data['campaign_id'] != campaign_id:
        response['error'].append("code_id is not associated with campaign_id provided")

    write_success = False
    if len(response['error']) == 0:
        response = {
            "redeemed": True,
            "status": code_data['status'],
            "total": code_data['total'],
            "remaining": code_data['remaining'] - 1,
        }

        # redeem code
        main.codes.append_to_history(data['code_id'], "Redeemed: " + unicode(shareddefs.appuuid()))
        code_data['remaining'] -= 1
        if code_data['remaining'] == 0:
            code_data['status'] = "redeemed"
        write_success = main.codes.set_data(data['code_id'], code_data)

    if write_success is True:  # updates campaign codes_data
        return response
    else:
        response['redeemed'] = False
        return response


class Redeem(Resource):
    """ Validates code data """
    @shareddefs.campaigns_api_token_required
    def post(self, campaign_id):
        args = parser.parse_args()
        data = {
            'code_id': args['code_id'],
            'api_key': args['api_key'],
            'code': args['code'],
            'friendly_code': args['friendly_code'],
            'transaction_amount': args['transaction_amount'],
            'transaction_currency': args['transaction_currency'],
        }
        validation_response = main.validate.validate_data(data)
        if validation_response['valid'] is True:
            response = redeem_data(data, campaign_id)
            if response['redeemed'] is True:
                return response, 201
            else:
                return response, 400
        else:
            return validation_response, 400  # bad request


api.add_resource(Redeem, '/redeem/<string:campaign_id>')
