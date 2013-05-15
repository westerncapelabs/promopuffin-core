from flask.ext.restful import reqparse, Resource, abort
from app import api

campaign_data = {}

parser = reqparse.RequestParser()
parser.add_argument('campaign_id', type=int) 
parser.add_argument('name', type=str)
parser.add_argument('start', type=str)#TODO
parser.add_argument('end', type=str)#TODO

def abort_campaign_not_found(campaign_id):
    if campaign_id not in campaign_data:
        abort(404, message="Campaign {} doesn't exist".format(campaign_id))

class Campaigns(Resource):
	def get(self):
		""" returns list of all campaigns """
		return campaign_data

	def post(self):
		""" saves a new campaign """
		args = parser.parse_args()
        campaign_id = 'uuid_%d' % (len(campaign_data) + 1)
        campaign_data[campaign_id] = {
            'campaign_id': args['campaign_id'],
            'name': args['name'],
            "start": args['start'],
            "end": args['end'],
            'status': args['status'],
        }
        return campaign_data[campaign_id], 201

api.add_resource(Campaigns, '/campaigns')

# class CampaignSearch(Resource):
# 	def get(self):
# 		"""take q and search Campaigns based on search parameters"""
		

# api.add_resource(Campaigns, '/campaigns/search')

class Campaign(Resource):
	""" For an individual Campaign"""
    def get(self, campaign_id):
        """ Just one campaign detail """
        abort_campaign_not_found(campaign_id)
        return campaign_data[campaign_id], 200

    def delete(self, campaign_id):
        abort_campaign_not_found(campaign_id)
        del campaign_data[campaign_id]
        return '', 204

    def put(self, campaign_id):
        args = parser.parse_args()
        campaign = {
            'campaign_id': args['campaign_id'],
            'name': args['name'],
            "start": args['start'],
            "end": args['end'],
            'status': args['pending'],
        }
        abort_campaign_not_found(campaign_id)
        campaign_data[campaign_id] = campaign
        return campaign, 201

api.add_resource(Campaign, '/campaigns/<string:campaign_id>')

class CampaignStatus(Resource):
	"""For status of campaign """
	def get(self,campaign_id):
		"""returns status of just one campaign """
		abort_campaign_not_found(campaign_id)
		return campaign_data[campaign_id], 200

	def post(self, campaign_id, status):
		"""request status change to pending,running,halted"""
		abort_campaign_not_found(campaign_id)
		campaign_data[campaign_id]=status
		return campaign_data[campaign_id], 201

api.add_resource(Campaign, '/campaigns/<string:campaign_id>/status')