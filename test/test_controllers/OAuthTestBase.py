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

    def run_with_token(self, func: Callable[[Client], Response], token: str):
        """
        Will run a callable on a test_client, with a provided token. This
        will help set up the session context properly. Will return the response.
        """
        with self.client as client:
            with client.session_transaction() as session:
                session["token"] = token
            response = func(client)

        return response


    @classmethod
    def tearDown(cls) -> None:
        db.session.remove()
        db.drop_all()

        cls.app_context.pop()
