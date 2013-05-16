from flask.ext.restful import reqparse, Resource, abort
from app import api

from shareddefs import appuuid

codes_data = {}

parser = reqparse.RequestParser()
parser.add_argument('code', type=str)
parser.add_argument('friendly_code', type=str)
parser.add_argument('type', type=str)
parser.add_argument('description', type=str)
parser.add_argument('status', type=str, default="unused")
parser.add_argument('value_type', type=str)
parser.add_argument('value_amount', type=float, default=0)
parser.add_argument('value_currency', type=str, default="ZAR")
parser.add_argument('minimum', type=float, default=0)
parser.add_argument('minimum_currency', type=str, default="ZAR")


def abort_code_not_found(code_id):
    if code_id not in codes_data:
        abort(404, message="Code {} doesn't exist".format(code_id))


class Codes(Resource):
    def get(self):
        """ lists all codes """
        return codes_data

    def post(self):
        """ saves a new code """
        args = parser.parse_args()
        code_id = appuuid()
        codes_data[code_id] = {
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
        }
        return codes_data[code_id], 201

api.add_resource(Codes, '/codes')