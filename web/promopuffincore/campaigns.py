from flask.ext.restful import reqparse, Resource, abort
from app import api
from datetime import datetime

import shareddefs

campaign_data = {}

parser = reqparse.RequestParser()
parser.add_argument('name', type=unicode)
parser.add_argument('start', type=unicode, default=''+datetime.utcnow().isoformat())
parser.add_argument('end', type=unicode, default=''+datetime.utcnow().isoformat())
parser.add_argument('status', type=unicode, default="pending")
parser.add_argument('account_id', type=unicode)


def abort_campaign_not_found(campaign_id):
    if campaign_id not in campaign_data:
        abort(404, message="Campaign {} doesn't exist".format(campaign_id))


class Campaigns(Resource):
    @shareddefs.api_token_required
    def get(self):
        """ returns list of all campaigns """
        return campaign_data

    @shareddefs.api_token_required
    def post(self):
        """ saves a new campaign """
        args = parser.parse_args()
        campaign_id = 'uuid_%d' % (len(campaign_data) + 1)
        # campaign_id = appuuid()
        campaign_data[campaign_id] = {
            'name': args['name'],
            "start": args['start'],
            "end": args['end'],
            'status': args['status'],
            'account_id': args['account_id'],
        }
        return campaign_data[campaign_id], 201

api.add_resource(Campaigns, '/campaigns')

# class CampaignSearch(Resource):
# 	def get(self):
# 		"""take q and search Campaigns based on search parameters"""

# api.add_resource(Campaigns, '/campaigns/search')


class Campaign(Resource):
    """ For an individual Campaign """
    @shareddefs.api_token_required
    def get(self, campaign_id):
        """ Just one campaign detail """
        abort_campaign_not_found(campaign_id)
        return campaign_data[campaign_id], 200

    @shareddefs.api_token_required
    def delete(self, campaign_id):
        abort_campaign_not_found(campaign_id)
        del campaign_data[campaign_id]
        return 'Campaign Successfully Deleted', 204

    @shareddefs.api_token_required
    def put(self, campaign_id):
        args = parser.parse_args()
        campaign = {
            'name': args['name'],
            "start": args['start'],
            "end": args['end'],
            'status': args['status'],
            'account_id': args['account_id'],
        }
        abort_campaign_not_found(campaign_id)
        campaign_data[campaign_id] = campaign
        return campaign, 201

api.add_resource(Campaign, '/campaigns/<string:campaign_id>')


class CampaignStatus(Resource):
    """For status of campaign """
    @shareddefs.api_token_required
    def get(self, campaign_id):
        """returns status of just one campaign """
        abort_campaign_not_found(campaign_id)
        return campaign_data[campaign_id]['status'], 200

    @shareddefs.api_token_required
    def post(self, campaign_id):
        args = parser.parse_args()
        """request status change to pending,running,halted"""
        abort_campaign_not_found(campaign_id)
        campaign_data[campaign_id]['status'] = args['status']
        return campaign_data[campaign_id], 201

api.add_resource(CampaignStatus, '/campaigns/<string:campaign_id>/status')
