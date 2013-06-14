from flask.ext.restful import reqparse, Resource, abort
import main
from app import api

import shareddefs

codes_data = {}

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


def abort_code_not_found(code_id):
    if code_id not in codes_data:
        abort(404, message="Code {} doesn't exist".format(code_id))


def find_all_campaign_codes(campaign_id):
    temp_data = {}
    for code in codes_data.itervalues():
        if campaign_id == code['campaign_id']:
            temp_data[len(codes_data) + 1] = dict(code)

    return temp_data


def get_data(code_id):
    abort_code_not_found(code_id)
    return dict(codes_data[code_id])


def set_data(code_id, data):
    abort_code_not_found(code_id)
    codes_data[code_id] = data
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


def append_to_history(code_id, history_msg):
    abort_code_not_found(code_id)
    code = codes_data[code_id]
    code['history_msg'].append(history_msg)


class Codes(Resource):
    @shareddefs.campaigns_api_token_required
    def get(self, campaign_id):
        """ lists all codes """
        return find_all_campaign_codes(campaign_id)

    @shareddefs.campaigns_api_token_required
    def post(self, campaign_id):
        """ saves a new code """
        args = parser.parse_args()
        # code_id = 'uuid_%d' % (len(codes_data) + 1)
        code_id = shareddefs.appuuid()

        # validate input data
        errors = validate_new_codes_data(args)
        if len(errors) > 0:
            return errors, 400

        codes_data[code_id] = {
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
        codes_data[code_id]["history_msg"].append("Initialised on:" + unicode(shareddefs.unix_timestamp()))
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

        # validate input data
        errors = validate_new_codes_data(args)
        if len(errors) > 0:
            return errors, 400

        abort_code_not_found(code_id)
        code = codes_data[code_id]

        code['campaign_id'] = campaign_id
        code['code'] = args['code']
        code['friendly_code'] = args['friendly_code']
        code["description"] = args['description']
        code["status"] = args['status']
        code["value_type"] = args['value_type']
        code["value_amount"] = args['value_amount']
        code["value_currency"] = args['value_currency']
        code["minimum"] = args['minimum']
        code["total"] = args['total']
        if "history_msg" in args:
            code['history_msg'].append(args['history_msg'])
        else:
            code['history_msg'].append("Updated: " + unicode(shareddefs.unix_timestamp()))
        code["remaining"] = args['remaining']

        codes_data[code_id] = code
        return code, 201

    @shareddefs.campaigns_api_token_required
    def delete(self, campaign_id, code_id):
        abort_code_not_found(code_id)
        del codes_data[code_id]
        return 'Code Successfully Deleted', 204

api.add_resource(Code, '/campaigns/<string:campaign_id>/codes/<string:code_id>')
