import unittest
import tempfile
from promopuffincore import main, accounts
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
        accounts.accounts_data = test_data.data_accounts_data
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
        assert "mike+testpromopuffin@westerncapelabs.com" in rv.data

    def test_accounts_add_new(self):
        rv = self.app.post("/accounts", data=test_data.data_accounts_post_good)
        assert "mike+testpromopuffin@westerncapelabs.com" in rv.data

    def test_accounts_account_not_found(self):
        rv = self.app.get('/accounts/uuid_90j0j0j')
        assert rv.status_code == 404

    def test_accounts_account_found(self):
        rv = self.app.get('/accounts/uuid_1')
        assert rv.status_code == 200
        assert "user1@example.com" in rv.data

    # def test_accounts_account_delete(self):
    #     rv = self.app.delete('/accounts/uuid_1')
    #     assert rv.status_code == 204
    #     rv = self.app.get('/accounts/uuid_1')
    #     assert rv.status_code == 404


if __name__ == '__main__':
    unittest.main()
