from flask import g
from flask.ext.restful import reqparse, Resource, abort
from app import api
from datetime import datetime

import main
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


class Campaigns(Resource):
    @shareddefs.campaigns_api_token_required
    def get(self):
        """ returns list of all campaigns """
        return get_bucket_list()

    @shareddefs.campaigns_api_token_required
    def post(self):
        """ saves a new campaign """
        args = parser.parse_args()

        # validate dates
        if args['start'] > args['end']:
            return "Start datetime starts after end datetime", 400

        campaign_data = {
            'name': args['name'],
            "start": args['start'],
            "end": args['end'],
            'status': args['status'],
            'account_id': args['account_id'],
        }

        # store to DB
        campaign_id = campaign_store(campaign_data)

        return campaign_data, 201

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
        campaign_exists(campaign_id)
        return campaign_load(campaign_id), 200

    @shareddefs.campaigns_api_token_required
    def delete(self, campaign_id):
        campaign_exists(campaign_id)
        campaign_delete(campaign_id)
        return 'Campaign Successfully Deleted', 204

    @shareddefs.campaigns_api_token_required
    def put(self, campaign_id):
        args = parser.parse_args()

        # validate dates
        if args['start'] > args['end']:
            return "Start datetime starts after end datetime", 400

        campaign_exists(campaign_id)
        campaign = {
            'name': args['name'],
            "start": args['start'],
            "end": args['end'],
            'status': args['status'],
            'account_id': args['account_id'],
        }

        # save to DB
        campaign_store(campaign, campaign_id)

        return campaign, 201

api.add_resource(Campaign, '/campaigns/<string:campaign_id>')


class CampaignStatus(Resource):
    """For status of campaign """
    @shareddefs.campaigns_api_token_required
    def get(self, campaign_id):
        """returns status of just one campaign """
        campaign_exists(campaign_id)
        return campaign_load(campaign_id)['status'], 200

    @shareddefs.campaigns_api_token_required
    def post(self, campaign_id):
        args = status_parser.parse_args()

        """request status change to pending,running,halted"""
        campaign_exists(campaign_id)
        campaign = campaign_load(campaign_id)
        campaign['status'] = args['status']
        temp_id = campaign_store(campaign, campaign_id)
        campaign_item = campaign_load(temp_id)

        return campaign_item, 201

api.add_resource(CampaignStatus, '/campaigns/<string:campaign_id>/status')


#####################
# DB Helper Functions
#####################


def campaign_exists(campaign_id):
    """ Check campaign exists - return True/False """
    bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'campaigns')
    if not bucket_data.get(campaign_id).exists():
        abort(404, message="Campaign {} doesn't exist".format(campaign_id))
    else:
        return True


# Save new and update (as far I can tell)
def campaign_store(data, campaign_id=False):
    """ Stores the data object passed in to the db, returns new key if wasn't passed one """
    # Choose a bucket to store our data in
    bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'campaigns')
    # Supply a key to store our data under
    if not campaign_id:
        campaign_id = shareddefs.appuuid()
        data_item = bucket_data.new(campaign_id, data=data)
    else:
        if campaign_exists(campaign_id):
            data_item = bucket_data.get(campaign_id)
            temp = data_item.get_data()
            temp.update(data)
            data_item.set_data(temp)
    data_item.store()
    return campaign_id


def campaign_load(campaign_id):
    """ Loads the campaign from db and returns the resulting data """
    if campaign_exists(campaign_id):
        bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'campaigns')
        data_item = bucket_data.get(campaign_id)
        return data_item.get_data()
    else:
        pass  # campaign_exists will handle errors for us


def campaign_delete(campaign_id):
    """ Removes the campaign from the bucket. """
    bucket_data = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'campaigns')
    if bucket_data.get(campaign_id).exists():
        bucket_data.get(campaign_id).delete()
        return True
    else:
        return False


def get_bucket_list():
    bucket = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'campaigns')
    bucket_keys = bucket.get_keys()
    response = {}
    for key in bucket_keys:
        response[key] = bucket.get(key).get_data()
    return response


def clear_bucket():
    bucket = g.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + 'accounts')
    bucket_keys = bucket.get_keys()
    for key in bucket_keys:
        bucket.get(key).delete()
    return "Deleted all values from accounts bucket..."
