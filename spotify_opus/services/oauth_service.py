import json
import os
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Optional

import requests
from flask import session, redirect, url_for, has_request_context, current_app
from requests import Request, Response

from spotify_opus import db
from spotify_opus.models.User import User

INVALID_TOKEN = "Please delete .json token file and re-attempt operation."
SPOTIFY_BASE_AUTH_URL = 'https://accounts.spotify.com'


class VerifyUser:
    """ This decorator provides an auth header and user information to
    any function it wraps via the req_header and user variables. Any
    wrapped function MUST accept these arguments as parameters.

    If there is no request context, it will instead pull from the .env
    variables to produce a valid token. This means that this decorator
    can be used regardless of the context universally throughout the
    application.
    """

    def __init__(self, admin: bool = False):

        self.admin = admin

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if has_request_context() and 'token' not in session:
                return redirect(url_for("auth.log_in"))
            elif not has_request_context():
                token = get_json_token()
            else:
                token = session["token"]

            req_header = get_auth_header(token)

            response = requests.get("https://api.spotify.com/v1/me",
                                    headers=req_header)

            if not response.ok and not has_request_context():
                raise RuntimeError(INVALID_TOKEN)
            elif not response.ok:
                return redirect(url_for("auth.log_in"))

            user_data = response.json()
            user = create_admin_user(user_data)

            if self.admin and not user:
                return redirect(url_for("auth.log_in"))
            elif not user:
                user = create_user(user_data)

            return func(*args, req_header=req_header, user=user, **kwargs)

        return wrapper


def create_admin_user(user_data: dict) -> Optional[User]:
    """Takes the user object from the Spotify API and
    queries the database to check if the user is an administrator.
    If so, returns the User model for it, or None if user is not an
    admin."""

    user_ext_id = user_data["id"]
    query = db.session.query(User)
    query = query.filter(User.external_id == user_ext_id)
    user = query.first()

    return user


def create_user(user_data: dict) -> User:
    """Creates a brand new user from the raw Spotify user object."""
    user = User()
    user.admin = False
    user.name = user_data["display_name"]
    user.external_id = user_data["id"]
    return user


def get_authorization_url() -> Optional[str]:
    """Prepares the url for the 1st phase of the auth code flow.
    Requires the application context.
    """
    redirect_url = current_app.config['REDIRECT_URL']
    params = {
        "client_id": current_app.config["SPOTIFY_CLIENT_ID"],
        "response_type": "code",
        "redirect_uri": f"{redirect_url}/auth/callback"
    }
    return Request("GET", f"{SPOTIFY_BASE_AUTH_URL}/authorize",
                   params=params).prepare().url


def process_callback(code: str) -> Response:
    """Will process a call back operation. Takes a code string
    and return the response from the 2nd phas of the auth flow.
    """
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    redirect_url = current_app.config["REDIRECT_URL"]

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": f"{redirect_url}/auth/callback",
        "client_id": current_app.config["SPOTIFY_CLIENT_ID"],
        "client_secret": current_app.config["SPOTIFY_CLIENT_SECRET"]
    }

    return requests.post(f"{SPOTIFY_BASE_AUTH_URL}/api/token",
                         data=data, headers=headers)


def get_json_token(admin=False) -> str:
    """Loads an access token from file storage, with the 'TOKEN' .env variables.
    If no cached file is present it will create a new one. Returns an access
    token."""
    if admin:
        token_filepath = current_app.config["ADMIN_TOKEN_FILEPATH"]
    else:
        token_filepath = current_app.config["BASIC_TOKEN_FILEPATH"]

    if Path(token_filepath).is_file():
        try:
            access_token = load_json_token(token_filepath)
        except Exception:
            raise RuntimeError(INVALID_TOKEN)
    else:
        access_token = update_json_token(token_filepath)

    return access_token


def load_json_token(token_filepath) -> str:
    """Loads the token from file storage and updates if necessary.
    Will throw an error if file is corrupted. """
    with open(token_filepath, "r") as file:
        data = json.load(file)

    now = datetime.now().timestamp()
    if data["expires_at"] < now:
        return update_json_token(token_filepath)
    else:
        return data["access_token"]


def update_json_token(token_filepath, admin=False):
    """Creates brand new data for token storage and persists it."""
    expiry = int(datetime.now().timestamp()) + 3600

    if admin:
        refresh_token = current_app.config["ADMIN_REFRESH_TOKEN"]
    else:
        refresh_token = current_app.config["BASIC_REFRESH_TOKEN"]

    access_token = get_new_token(refresh_token)
    dump_json_token(expiry, refresh_token, access_token, token_filepath)
    return access_token


def dump_json_token(expiry: int, refresh_token: str,
                    access_token: str, token_filepath: str) -> None:
    """ Will dump token information to the designated location as per
    the .env file. """

    data = {
        "expires_at": expiry,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

    with open(token_filepath, "w") as file:
        json.dump(data, file)


def get_new_token(refresh_token: str):
    """Will query the Spotify API for a new access token from a
    refresh token following the protocol of the official API.
    Will raise an exception if """

    url = "https://accounts.spotify.com/api/token"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET")
    }

    response = requests.post(url, data=data, headers=headers)

    if not response.ok:
        raise ValueError("Error when refreshing token from Spotify, "
                         "ensure that the refresh token is valid.")

    return response.json()["access_token"]


def get_auth_header(token: str):
    return {
        "Authorization": f"Bearer {token}"
    }
