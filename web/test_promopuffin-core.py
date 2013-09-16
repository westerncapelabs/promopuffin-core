import unittest
from promopuffincore import main, accounts, campaigns, codes
import test_data
import riak
import json


class PromoPuffinCoreTestCase(unittest.TestCase):
    def clear_db(self):
        # clear 'test_' buckets
        self.clear_bucket('accounts')
        self.clear_bucket('campaigns')
        self.clear_bucket('codes')

    def clear_bucket(self, bucket):
        bucket = self.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + bucket)
        bucket_keys = bucket.get_keys()
        for key in bucket_keys:
            bucket.get(key).delete()
        return True

    def bucket_item_store(self, bucket_name, data, item_id=False):
        """ Stores the data object passed in to the db, retunrs new key if wasn't passed one """
        # Choose a bucket to store our data in
        bucket_data = self.rc.bucket(main.app.config['RIAK_BUCKET_PREFIX'] + bucket_name)
        # Supply a key to store our data under
        if not item_id:
            item_id = main.shareddefs.appuuid()
            data_item = bucket_data.new(item_id, data=data)
        else:
            data_item = bucket_data.get(item_id)
            data_item.set_data(data)
        data_item.store()
        return item_id

    def init_db(self):
        # populate 'test_' buckets
        for account in test_data.data_accounts_data:
            self.bucket_item_store('accounts', test_data.data_accounts_data[account], account)
        for campaign in test_data.data_campaigns_data:
            self.bucket_item_store('campaigns', test_data.data_campaigns_data[campaign], campaign)
        for code in test_data.data_campaigns_codes_data:
            self.bucket_item_store('codes', test_data.data_campaigns_codes_data[code], code)

    def setUp(self):
        # db_conf = {
        #     'name': '',
        #     'engine': 'SqliteDatabase',
        #     'check_same_thread': False,
        # }
        # self.db_fd, db_conf["name"] = tempfile.mkstemp()
        # main.app.config['DATABASE'] = db_conf
        main.app.config['TESTING'] = True
        main.app.config['RIAK_BUCKET_PREFIX'] = 'promopuffin_core_test_'
        self.rc = riak.RiakClient(host=main.app.config['RIAK_HOST'], port=main.app.config['RIAK_PORT'], prefix=main.app.config['RIAK_PREFIX'], transport_class=main.app.config['RIAK_TRANSPORT_CLASS'])
        # accounts.accounts_data = dict(test_data.data_accounts_data)
        # campaigns.campaigns_data = dict(test_data.data_campaigns_data)
        # codes.codes_data = dict(test_data.data_campaigns_codes_data)
        self.app = main.app.test_client()
        self.init_db()

    def tearDown(self):
        self.clear_db()

    # """ general tests """
    # def test_404_render(self):
    #     rv = self.app.get('/kldjfljsdlkfjsdlkjfdslkj')  # Should never validate!
    #     assert '404' in rv.data  # Should be the <title> of the page

    # def test_hello_world(self):
    #     rv = self.app.get('/heartbeat')
    #     assert 'Hello World!' in rv.data  # Should be the <title> of the page

    # """ Accounts Tests """
    # def test_accounts_account_login_success(self):
    #     rv = self.app.post("/accounts?auth=somekey", data=test_data.data_accounts_login_good)
    #     account_data = json.loads(rv.data)
    #     account_data["password"] = test_data.data_accounts_login_good["password"]
    #     rv = self.app.post('/accounts/login', data=account_data)
    #     assert rv.status_code == 201

    # def test_accounts_account_login_fail(self):
    #     rv = self.app.post("/accounts?auth=somekey", data=test_data.data_accounts_login_good)
    #     account_data = json.loads(rv.data)
    #     account_data["password"] = test_data.data_accounts_login_bad["password"]
    #     rv = self.app.post('/accounts/login', data=account_data)
    #     assert rv.status_code == 401
    #     assert "Unauthorized: Incorrect username and password match" in rv.data

    # def test_accounts_account_login_no_data(self):
    #     rv = self.app.post("/accounts?auth=somekey", data=test_data.data_accounts_login_good)
    #     account_data = json.loads(rv.data)
    #     rv = self.app.post('/accounts/login', data=account_data)
    #     assert rv.status_code == 400

    # def test_accounts_list(self):
    #     rv = self.app.get('/accounts?auth=somekey')
    #     assert "user1@example.com" in rv.data

    # def test_accounts_add_new(self):
    #     rv = self.app.post("/accounts?auth=somekey", data=test_data.data_accounts_post_good)
    #     assert "mike+testpromopuffin@westerncapelabs.com" in rv.data

    # def test_accounts_account_found(self):
    #     rv = self.app.get('/accounts/uuid_1?auth=somekey')
    #     assert rv.status_code == 200
    #     assert "user1@example.com" in rv.data

    # def test_accounts_account_not_found(self):
    #     rv = self.app.get('/accounts/uuid_90j0j0j?auth=somekey')
    #     assert rv.status_code == 404

    # def test_accounts_account_delete_found(self):
    #     rv = self.app.delete('/accounts/uuid_1?auth=somekey')
    #     assert rv.status_code == 204
    #     rv = self.app.get('/accounts/uuid_1?auth=somekey')
    #     assert rv.status_code == 404

    # def test_accounts_account_delete_not_found(self):
    #     rv = self.app.delete('/accounts/uuid_342fhdjs41?auth=somekey')
    #     assert rv.status_code == 404

    # def test_accounts_account_put_found(self):
    #     rv = self.app.put('/accounts/uuid_1?auth=somekey', data=test_data.data_accounts_put_good)
    #     assert rv.status_code == 201
    #     rv = self.app.get('/accounts/uuid_1?auth=somekey')
    #     assert rv.status_code == 200
    #     assert "user1@example.com" in rv.data

    # def test_accounts_account_put_not_found(self):
    #     rv = self.app.put('/accounts/uuid_4234jhkjhk4?auth=somekey', data=test_data.data_accounts_put_good)
    #     assert rv.status_code == 404

    # def test_accounts_list_not_authenticated(self):
    #     rv = self.app.get('/accounts?auth=some3424gegkey')
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_accounts_account_post_not_authenticated(self):
    #     rv = self.app.post('/accounts?auth=somedskfjslf', data=test_data.data_accounts_post_good)
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_accounts_account_post_no_data(self):
    #     rv = self.app.post('/accounts?auth=somekey', data="")
    #     assert rv.status_code == 400

    # def test_accounts_account_get_not_authenticated(self):
    #     rv = self.app.get('/accounts/uuid_1?auth=somedskfjslf')
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_accounts_account_put_not_authenticated(self):
    #     rv = self.app.put('/accounts/uuid_1?auth=somedskfjslf', data=test_data.data_accounts_put_good)
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_accounts_account_delete_not_authenticated(self):
    #     rv = self.app.delete('/accounts/uuid_1?auth=somedskfjslf')
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_accounts_account_put_no_data(self):
    #     rv = self.app.put('/accounts/uuid_1?auth=thisandthat', data="")
    #     assert rv.status_code == 400

    """ Campaigns Tests """
    # def test_campaigns_list(self):
    #     rv = self.app.get('/campaigns?auth=somekey')
    #     assert "Campaign3" in rv.data

    # def test_campaigns_add_new(self):
    #     rv = self.app.post("/campaigns?auth=somekey", data=test_data.data_campaigns_post_good)
    #     assert "OneTheWayCampaign" in rv.data

    # def test_campaigns_campaign_not_found(self):
    #     rv = self.app.get('/campaigns/uuid_66hj768?auth=somekey')
    #     assert rv.status_code == 404

    # def test_campaigns_campaign_found(self):
    #     rv = self.app.get('/campaigns/uuid_1?auth=somekey')
    #     assert rv.status_code == 200
    #     assert "Campaign1" in rv.data

    # def test_campaigns_campaign_delete_found(self):
    #     rv = self.app.delete('/campaigns/uuid_1?auth=somekey')
    #     assert rv.status_code == 204
    #     rv = self.app.get('/campaigns/uuid_1?auth=somekey')
    #     assert rv.status_code == 404

    # def test_campaigns_campaign_delete_not_found(self):
    #     rv = self.app.delete('/campaigns/uuid_342jh4khk231?auth=somekey')
    #     assert rv.status_code == 404

    # def test_campaigns_campaign_put_found(self):
    #     rv = self.app.put('/campaigns/uuid_1?auth=somekey', data=test_data.data_campaigns_put_good)
    #     assert rv.status_code == 201
    #     assert "2013-06-21T19:12:04.781462" in rv.data
    #     rv = self.app.get('/campaigns/uuid_1?auth=somekey')
    #     assert rv.status_code == 200
    #     assert "OneTheWayCampaign" in rv.data

    # def test_campaigns_campaign_put_not_found(self):
    #     rv = self.app.put('/campaigns/uuid_43420jkds21?auth=somekey', data=test_data.data_campaigns_put_good)
    #     assert rv.status_code == 404

    # def test_campaigns_campaign_status_list_found(self):
    #     rv = self.app.get('/campaigns/uuid_2/status?auth=somekey')
    #     assert rv.status_code == 200
    #     assert "running" in rv.data

    # def test_campaigns_campaign_status_list_not_found(self):
    #     rv = self.app.get('/campaigns/uuid_3423jh2k1/status?auth=somekey')
    #     assert rv.status_code == 404

    # def test_campaigns_campaign_status_update_found(self):
    #     rv = self.app.post('/campaigns/uuid_1/status?auth=somekey', data=test_data.data_campaigns_status_post_good)
    #     assert rv.status_code == 201
    #     assert "halted" in rv.data

    # def test_campaigns_campaign_status_update_not_found(self):
    #     rv = self.app.post('/campaigns/uuid_3429kjkj31/status?auth=somekey', data=test_data.data_campaigns_status_post_good)
    #     assert rv.status_code == 404

    # def test_campaigns_list_not_authenticated(self):
    #     rv = self.app.get('/campaigns?auth=some3424gegkey')
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_campaigns_campaign_post_not_authenticated(self):
    #     rv = self.app.post('/campaigns?auth=somedskfjslf', data=test_data.data_campaigns_post_good)
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_campaigns_campaign_post_no_data(self):
    #     rv = self.app.post('/campaigns?auth=somekey', data="")
    #     assert rv.status_code == 400

    # def test_campaigns_campaign_get_not_authenticated(self):
    #     rv = self.app.get('/campaigns/uuid_1?auth=somedskfjslf')
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_campaigns_campaign_put_not_authenticated(self):
    #     rv = self.app.put('/campaigns/uuid_1?auth=somedskfjslf', data=test_data.data_campaigns_put_good)
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_campaigns_campaign_no_campaign_id(self):
    #     rv = self.app.put('/campaigns?auth=somekey', data=test_data.data_campaigns_put_good)
    #     assert rv.status_code == 405

    # def test_campaigns_campaign_put_no_data(self):
    #     rv = self.app.put('/campaigns/uuid_1?auth=somekey', data="")
    #     assert rv.status_code == 400

    # def test_campaigns_campaign_delete_not_authenticated(self):
    #     rv = self.app.delete('/campaigns/uuid_1?auth=somedskfjslf')
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_campaigns_campaign_status_not_authenticated(self):
    #     rv = self.app.get('/campaigns/uuid_1/status?auth=some3432423f22key')
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_campaigns_campaign_status_post_not_authenticated(self):
    #     rv = self.app.post('/campaigns/uuid_1/status?auth=some3432423f22key', data=test_data.data_campaigns_status_post_good)
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_campaigns_campaign_status_no_data(self):
    #     rv = self.app.post('/campaigns/uuid_1/status?auth=somekey', data="")
    #     assert rv.status_code == 400

    # def test_campaigns_campaign_status_no_campaign_id(self):
    #     rv = self.app.post('/campaigns/status?auth=somekey', data=test_data.data_campaigns_status_post_good)
    #     assert rv.status_code == 405  # method not allowed

    # def test_campaigns_campaign_put_bad(self):
    #     rv = self.app.put('/campaigns/uuid_1?auth=somekey', data=test_data.data_campaigns_put_bad)
    #     assert "Start datetime starts after end datetime" in rv.data

    # """ Codes Tests """
    # def test_campaigns_campaign_codes_list(self):
    #     rv = self.app.get('/campaigns/uuid_3/codes?auth=thisandthat')
    #     assert "QWZ-EMD-ABCDEF" in rv.data

    # def test_campaigns_campaign_codes_list_not_authenticated(self):
    #     rv = self.app.post('/campaigns/uuid_1/codes?auth=some3432423f22key')
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_campaigns_campaign_codes_add_new(self):
    #     rv = self.app.post('/campaigns/uuid_1/codes?auth=somekey', data=test_data.data_campaigns_codes_post_good)
    #     assert rv.status_code == 201
    #     assert "ABC-DEF-GIJKLM" in rv.data

    # def test_campaigns_campaign_codes_code_post_no_data(self):
    #     rv = self.app.post('campaigns/uuid_1/codes?auth=somekey', data="")
    #     assert rv.status_code == 400

    # def test_campaigns_campaign_codes_post_not_authenticated(self):
    #     rv = self.app.post('/campaigns/uuid_1/codes?auth=some3432423f22key', data=test_data.data_campaigns_codes_post_good)
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_campaigns_campaign_codes_code_found(self):
    #     rv = self.app.get('/campaigns/uuid_1/codes/uuid_1?auth=somekey')
    #     assert rv.status_code == 200
    #     assert "ACT-EKL-ABCDEF" in rv.data

    # def test_campaigns_campaign_codes_code_found_not_authenticated(self):
    #     rv = self.app.get('/campaigns/uuid_1/codes/uuid_1?auth=some3432423f22ke')
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_campaigns_campaign_codes_code_not_found(self):
    #     rv = self.app.get('/campaigns/uuid_1/codes/uuid_34532errwr?auth=somekey')
    #     assert rv.status_code == 404

    # def test_campaigns_campaign_codes_code_delete_found(self):
    #     rv = self.app.delete('/campaigns/uuid_1/codes/uuid_1?auth=somekey')
    #     assert rv.status_code == 204
    #     rv = self.app.get('/campaigns/uuid_1/codes/uuid_1?auth=somekey')
    #     assert rv.status_code == 404

    # def test_campaigns_campaign_codes_code_delete_not_authenticated(self):
    #     rv = self.app.delete('/campaigns/uuid_1/codes/uuid_1?auth=some3432423f22key')
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_campaigns_campaign_codes_code_delete_not_found(self):
    #     rv = self.app.delete('/campaigns/uuid_1/codes/uuid_342dfs1?auth=somekey')
    #     assert rv.status_code == 404

    # def test_campaigns_campaign_codes_code_put_found(self):
    #     rv = self.app.put('/campaigns/uuid_1/codes/uuid_1?auth=somekey', data=test_data.data_campaigns_codes_put_good)
    #     assert rv.status_code == 201
    #     rv = self.app.get('/campaigns/uuid_1/codes/uuid_1?auth=somekey')
    #     assert rv.status_code == 200
    #     assert "redeemed" in rv.data

    # def test_campaigns_campaign_codes_code_put_not_authenticated(self):
    #     rv = self.app.put('/campaigns/uuid_1/codes/uuid_1', data=test_data.data_campaigns_codes_put_good)
    #     assert "Unauthorized" in rv.data
    #     assert rv.status_code == 401

    # def test_campaigns_campaign_codes_code_put_not_found(self):
    #     rv = self.app.put('/campaigns/uuid_1/codes/uuid_432dfs341?auth=somekey', data=test_data.data_campaigns_codes_put_good)
    #     assert rv.status_code == 404

    # def test_campaigns_campaign_codes_put_no_data(self):
    #     rv = self.app.put('/campaigns/uuid_1/codes/uuid_1?auth=somekey', data="")
    #     assert rv.status_code == 400

    # def test_campaigns_campaign_codes_no_campaign_id(self):
    #     rv = self.app.put('/campaigns/codes/uuid_1?auth=thisandthat', data=test_data.data_campaigns_codes_put_good)
    #     assert rv.status_code == 404

    """ Validation Tests """
    def test_validate_success_percentage(self):
        rv = self.app.post('/validate', data=test_data.data_validation_post_percentage_good)
        assert rv.status_code == 201
        assert "true" in rv.data

    def test_validate_success_fixed(self):
        rv = self.app.post('/validate', data=test_data.data_validation_post_fixed_good)
        assert rv.status_code == 201
        assert "true" in rv.data

    def test_validate_fail(self):
        rv = self.app.post('/validate', data=test_data.data_validation_post_bad)
        assert rv.status_code == 400
        assert "false" in rv.data

    def test_validate_no_data(self):
        rv = self.app.post('/validate', data="")
        assert "Code None doesn't exist" in rv.data
        assert rv.status_code == 404

    # """ Redeemed Tests """
    # def test_redeem_percentage_success(self):
    #     rv = self.app.post('/redeem/uuid_3?auth=thisandthat', data=test_data.data_redeem_percentage_good)
    #     assert rv.status_code == 201
    #     assert "true" in rv.data

    # def test_redeem_percentage_success_admin_auth(self):
    #     rv = self.app.post('/redeem/uuid_3?auth=somekey', data=test_data.data_redeem_percentage_good)
    #     assert rv.status_code == 201
    #     assert "true" in rv.data

    # def test_redeem_percentage_fail(self):
    #     rv = self.app.post('/redeem/uuid_2?auth=thisandthat', data=test_data.data_redeem_percentage_bad)
    #     assert rv.status_code == 400
    #     assert "false" in rv.data

    # def test_redeem_fixed_success(self):
    #     rv = self.app.post('/redeem/uuid_3?auth=thisandthat', data=test_data.data_redeem_fixed_good)
    #     assert rv.status_code == 201
    #     assert "true" in rv.data

    # def test_redeem_auth_fail(self):
    #     rv = self.app.post('/redeem/uuid_1?auth=dskfsld9', data=test_data.data_redeem_percentage_good)
    #     assert rv.status_code == 401
    #     assert "Unauthorized" in rv.data

    # def test_redeem_no_data(self):
    #     rv = self.app.post('/redeem/uuid_1?auth=somekey', data="")
    #     assert "Code None doesn't exist" in rv.data
    #     assert rv.status_code == 404

    # def test_redeem_no_campaign_id(self):
    #     rv = self.app.post('/redeem?auth=somekey', data=test_data.data_redeem_percentage_good)
    #     assert rv.status_code == 404


if __name__ == '__main__':
    unittest.main()
