from werkzeug import Client

from spotify_opus.services.oauth_service import get_json_token
from test.test_controllers.OAuthTestBase import OAuthTestBase


class TestComposer(OAuthTestBase):

    def test_auth(self):
        """The purpose of this test is to make sure that users can't
        access the application without logging in first."""


        token = get_json_token()



    def request_page(self, method: str, path: str, token: str):

        def func(client: Client):
            if method == "GET":
                return client.get(path)
            elif method == "POST":
                return client.post(path)
            else:
                raise ValueError("Incorrect method supplied to request page method")

        response = self.client.get("/")
        self.assertEquals(response.status_code, 302,
                          "No token redirects user.")

        response = self.run_with_token(func, token)
        self.assertEquals(response.status_code, 200,
                          "Running with token doesn't redirect")
