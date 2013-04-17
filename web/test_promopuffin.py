import unittest
import promopuffin
import test_data


class PromoPuffinTestCase(unittest.TestCase):
    def setUp(self):
        #promopuffin.app.config['TESTING'] = True
        self.app = promopuffin.app.test_client()
        # self.data_auth = "TESTAUTHCODE"
        # self.data_auth_admin = "TESTAUTHADMINCODE"

    def tearDown(self):
        pass

    def test_404_render(self):
        rv = self.app.get('/kldjfljsdlkfjsdlkjfdslkj')  # Should never validate!
        assert '404' in rv.data  # Should be the <title> of the page

    def test_authentication_blockedroot(self):
        rv = self.app.get("/")  # All api calls require authentication of some sorts
        assert '401' in rv.data  # should be a nice error message

    def test_authentication_goodkey(self):
        rv = self.app.get("/auth?key=" + test_data.data_auth)
        assert 'Authorization successful' in rv.data  # should be provided to validated connection

    def test_authentication_badkey(self):
        rv = self.app.get("/auth?key=dsadsadasdasdeeeada")
        assert '401' in rv.data  # should be provided to validated connection

    def test_accounts_get_auth_badadminkey(self):
        rv = self.app.get("/accounts?key=" + test_data.data_auth)
        assert '401' in rv.data  # should not be able to GET this endpoint with non-admin key

    def test_accounts_get_auth_goodadminkey(self):
        rv = self.app.get("/accounts?key=" + test_data.data_auth_admin)
        assert "accounts" in rv.data  # should be an accounts array even if empty in response

    def test_accounts_post_auth_gooddata(self):
        rv = self.app.post("/accounts", data=test_data.data_accounts_post_good)
        assert "Account created" in rv.data

if __name__ == '__main__':
    unittest.main()
