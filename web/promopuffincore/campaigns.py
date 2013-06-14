from flask.ext.restful import reqparse, Resource, abort
from app import api
from datetime import datetime

import shareddefs

campaigns_data = {}

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=unicode, case_sensitive=True)
parser.add_argument('start', required=True, type=unicode, default=''+datetime.utcnow().isoformat())
parser.add_argument('end', required=True, type=unicode, default=''+datetime.utcnow().isoformat())
parser.add_argument('status', type=unicode, default="pending")
parser.add_argument('account_id', required=True, type=unicode, case_sensitive=True)

status_parser = reqparse.RequestParser()
status_parser.add_argument('status', required=True, type=unicode, default="pending")


def abort_campaign_not_found(campaign_id):
    if campaign_id not in campaigns_data:
        abort(404, message="Campaign {} doesn't exist".format(campaign_id))


# returns a copy of campaigns_data
def get_data(campaign_id):
    abort_campaign_not_found(campaign_id)
    return dict(campaigns_data[campaign_id])


class Campaigns(Resource):
    @shareddefs.campaigns_api_token_required
    def get(self):
        """ returns list of all campaigns """
        return campaigns_data

    @shareddefs.campaigns_api_token_required
    def post(self):
        """ saves a new campaign """
        args = parser.parse_args()

        # validate dates
        if args['start'] > args['end']:
            return "Start datetime starts after end datetime", 400

        campaign_id = shareddefs.appuuid()
        campaigns_data[campaign_id] = {
            'name': args['name'],
            "start": args['start'],
            "end": args['end'],
            'status': args['status'],
            'account_id': args['account_id'],
        }
        return campaigns_data[campaign_id], 201

api.add_resource(Campaigns, '/campaigns')

# class CampaignSearch(Resource):
# 	def get(self):
# 		"""take q and search Campaigns based on search parameters"""

# api.add_resource(Campaigns, '/campaigns/search')


class Campaign(Resource):
    """ For an individual Campaign """
    @shareddefs.campaigns_api_token_required
    def get(self, campaign_id):
        """ Just one campaign detail """
        abort_campaign_not_found(campaign_id)
        return campaigns_data[campaign_id], 200

    @shareddefs.campaigns_api_token_required
    def delete(self, campaign_id):
        abort_campaign_not_found(campaign_id)
        del campaigns_data[campaign_id]
        return 'Campaign Successfully Deleted', 204

    @shareddefs.campaigns_api_token_required
    def put(self, campaign_id):
        args = parser.parse_args()

        # validate dates
        if args['start'] > args['end']:
            return "Start datetime starts after end datetime", 400

        abort_campaign_not_found(campaign_id)
        campaign = campaigns_data[campaign_id]

        campaign['name'] = args['name']
        campaign["start"] = args['start']
        campaign["end"] = args['end']
        campaign['status'] = args['status']
        campaign['account_id'] = args['account_id']

        campaigns_data[campaign_id] = campaign

        return campaign, 201

api.add_resource(Campaign, '/campaigns/<string:campaign_id>')


class CampaignStatus(Resource):
    """For status of campaign """
    @shareddefs.campaigns_api_token_required
    def get(self, campaign_id):
        """returns status of just one campaign """
        abort_campaign_not_found(campaign_id)
        return campaigns_data[campaign_id]['status'], 200

    @shareddefs.campaigns_api_token_required
    def post(self, campaign_id):
        args = status_parser.parse_args()

        """request status change to pending,running,halted"""
        abort_campaign_not_found(campaign_id)
        campaigns_data[campaign_id]['status'] = args['status']
        return campaigns_data[campaign_id], 201

api.add_resource(CampaignStatus, '/campaigns/<string:campaign_id>/status')
