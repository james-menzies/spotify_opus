from flask import url_for
from werkzeug import Client

from test.test_controllers.OAuthTestBase import OAuthTestBase


class TestAuth(OAuthTestBase):
    """The premise of these tests are to ensure that users cannot access
    pages without being logged in or authorized as appropriate. """

    def request_page(self, method: str, path: str, admin: bool):

        def func(client: Client):
            if method == "GET":
                return client.get(path)
            elif method == "POST":
                return client.post(path)
            else:
                raise ValueError(
                    "Incorrect method supplied to request page method")

        if admin:
            token = self.admin_token
        else:
            token = self.basic_token

        response = self.client.get(path)
        self.assertEqual(response.status_code, 302,
                         "No token redirects user.")

        response = self.run_with_token(func, token)
        self.assertNotEqual(response.status_code, 302,
                            "Running with token doesn't redirect")

    def test_home(self):
        """The purpose of this test is to make sure that users can't
        access the application without logging in first."""

        self.request_page("GET", url_for("composer.get_all"), False)

    def test_create_composer(self):

        self.request_page("GET", url_for("composer.create_new"), True)
