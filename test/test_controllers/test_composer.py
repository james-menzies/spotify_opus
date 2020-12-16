from spotify_opus.services.oauth_service import get_json_token
from test.test_controllers.OAuthTestBase import OAuthTestBase


class TestComposer(OAuthTestBase):

    def test_auth(self):
        def func(client):
            return client.get("/composer/")

        token = get_json_token()

        response = self.client.get("/composer/")
        self.assertEquals(response.status_code, 302,
                          "No token redirects user.")

        response = self.run_with_token(func, token)
        self.assertEquals(response.status_code, 200,
                          "Running with token doesn't redirect")
