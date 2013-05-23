import unittest
import tempfile
from promopuffincore import main, accounts, campaigns, codes
import test_data


class PromoPuffinCoreTestCase(unittest.TestCase):
    def setUp(self):
        # db_conf = {
        #     'name': '',
        #     'engine': 'SqliteDatabase',
        #     'check_same_thread': False,
        # }
        # self.db_fd, db_conf["name"] = tempfile.mkstemp()
        # main.app.config['DATABASE'] = db_conf
        main.app.config['TESTING'] = True
        accounts.accounts_data = dict(test_data.data_accounts_data)
        campaigns.campaign_data = dict(test_data.data_campaigns_data)
        self.app = main.app.test_client()

    def tearDown(self):
        pass
        # os.close(self.db_fd)
        # os.unlink(main.app.config['DATABASE']['name'])

    def test_404_render(self):
        rv = self.app.get('/kldjfljsdlkfjsdlkjfdslkj')  # Should never validate!
        assert '404' in rv.data  # Should be the <title> of the page

    def test_hello_world(self):
        rv = self.app.get('/heartbeat')
        assert 'Hello World!' in rv.data  # Should be the <title> of the page

    def test_accounts_list(self):
        rv = self.app.get('/accounts')
        assert "user1@example.com" in rv.data

    def test_accounts_add_new(self):
        rv = self.app.post("/accounts", data=test_data.data_accounts_post_good)
        assert "mike+testpromopuffin@westerncapelabs.com" in rv.data

    def test_accounts_account_found(self):
        rv = self.app.get('/accounts/uuid_1')
        assert rv.status_code == 200
        assert "user1@example.com" in rv.data

    def test_accounts_account_not_found(self):
        rv = self.app.get('/accounts/uuid_90j0j0j')
        assert rv.status_code == 404

    def test_accounts_account_delete_found(self):
        rv = self.app.delete('/accounts/uuid_1')
        assert rv.status_code == 204
        rv = self.app.get('/accounts/uuid_1')
        assert rv.status_code == 404

    def test_accounts_account_delete_not_found(self):
        rv = self.app.delete('/accounts/uuid_342fhdjs41')
        assert rv.status_code == 404

    def test_accounts_account_put_found(self):
        rv = self.app.put('/accounts/uuid_1', data=test_data.data_accounts_put_good)
        assert rv.status_code == 201
        rv = self.app.get('/accounts/uuid_1')
        assert rv.status_code == 200
        assert "user1@example.com" in rv.data

    def test_accounts_account_put_not_found(self):
        rv = self.app.put('/accounts/uuid_4234jhkjhk4', data=test_data.data_accounts_put_good)
        assert rv.status_code == 404

    def test_campaigns_list(self):
        rv = self.app.get('/campaigns')
        assert "Campaign1" in rv.data

    def test_campaigns_add_new(self):
        rv = self.app.post("/campaigns", data=test_data.data_campaigns_post_good)
        assert "OneTheWayCampaign" in rv.data

    def test_campaigns_campaign_not_found(self):
        rv = self.app.get('/campaigns/uuid_66768')
        assert rv.status_code == 404

    def test_campaigns_found(self):
        rv = self.app.get('/campaigns/uuid_1')
        assert rv.status_code == 200
        assert "Campaign1" in rv.data

    def test_campaigns_delete_found(self):
        rv = self.app.delete('/campaigns/uuid_1')
        assert rv.status_code == 204
        rv = self.app.get('/campaigns/uuid_1')
        assert rv.status_code == 404

    def test_campaigns_delete_not_found(self):
        rv = self.app.delete('/campaigns/uuid_342jh4khk231')
        assert rv.status_code == 404

    def test_campaigns_put_found(self):
        rv = self.app.put('/campaigns/uuid_1', data=test_data.data_campaigns_put_good)
        assert "2013-06-21T19:12:04.781462" in rv.data
        rv = self.app.get('/campaigns/uuid_1')
        assert rv.status_code == 200
        assert "OneTheWayCampaign" in rv.data

    def test_campaigns_put_not_found(self):
        rv = self.app.put('/campaigns/uuid_43420jkds21', data=test_data.data_campaigns_put_good)
        assert rv.status_code == 404

    def test_campaigns_status_list_found(self):
        rv = self.app.get('/campaigns/uuid_1/status')
        assert rv.status_code == 200
        assert "running" in rv.data

    def test_campaigns_status_list_not_found(self):
        rv = self.app.get('/campaigns/uuid_3423jh2k1/status')
        assert rv.status_code == 404

    def test_campaigns_status_update_found(self):
        rv = self.app.post('/campaigns/uuid_1/status', data=test_data.data_campaigns_status_post_good)
        assert rv.status_code == 201
        assert "halted" in rv.data

    def test_campaigns_status_update_not_found(self):
        rv = self.app.post('/campaigns/uuid_3429kjkj31/status', data=test_data.data_campaigns_status_post_good)
        assert rv.status_code == 404

if __name__ == '__main__':
    unittest.main()
