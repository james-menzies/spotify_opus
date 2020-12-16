import os
import unittest
from typing import Callable

from flask import Flask, Response
from werkzeug import Client

from spotify_opus import db, create_app


class OAuthTestBase(unittest.TestCase):

    @classmethod
    def setUp(cls) -> None:
        os.environ["FLASK_ENV"] = "testing"
        cls.app: Flask = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

        runner = cls.app.test_cli_runner()
        db.create_all()
        result = runner.invoke(args=["manage", "reset", "--no-migrate"])
        if result.exit_code != 0:
            raise ValueError(result.stdout)

    def run_with_token(self, func: Callable[[Client], Response], token_file: str):
        """
        Will run a callable on a test_client, with a provided token. This
        will help set up the session context properly. Will return the response.
        """
        with self.client as client:
            with client.session_transaction() as session:
                session["token"] = token_file
            response = func(client)

        return response

    def test_token(self):
        token = "BQCZNpZumqnYlQgeEjI-kFQBFptpM0M4CYR9WU6fFCdfZsrUIJ1C1ENeFq0A-4jFFATCCEYFzPvin7RjAFF1LYLBwoS9u8HKN1Qkd-7Xh61LZF8btFLoFB4Qaw2Mw7ACAuNumSzJl1O9MjVmwQItPtmZ1xa-yJ9RLy_dTxc4PR3pbLIvrOSTkT6lzIwrZvW6cOAFpnshxePkzpJwwyaP_zAKC1CXNuUADpow1S0cLMFz6NmRF8J8JMq94ygTOM2SZqW6BuJZcjCr-k"
        response = self.run_with_token(lambda c: c.get("/"), token)
        print(response)
        self.run_with_token()

    @classmethod
    def tearDown(cls) -> None:
        db.session.remove()
        db.drop_all()

        cls.app_context.pop()
