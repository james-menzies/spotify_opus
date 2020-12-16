import json
import os
from datetime import datetime
from functools import wraps
from pathlib import Path

import requests
from flask import session, redirect, url_for, has_request_context, current_app

INVALID_TOKEN = "Please delete .json token file and re-attempt operation."


def verify_user(func):
    """ This decorator provides an auth header and user information to
    any function it wraps via the req_header and user variables. Any
    wrapped function MUST accept these arguments as parameters.

    If there is no request context, it will instead pull from the .env
    variables to produce a valid token. This means that this decorator
    can be used regardless of the context universally throughout the
    application.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        if has_request_context() and 'token' not in session:
            return redirect(url_for("auth.log_in"))
        elif not has_request_context():
            token = get_json_token()
        else:
            token = session["token"]

        req_header = get_auth_header(token)

        response = requests.get("https://api.spotify.com/v1/me", headers=req_header)

        if not response.ok and not has_request_context():
            raise RuntimeError(INVALID_TOKEN)
        elif not response.ok:
            return redirect(url_for("auth.log_in"))

        user = response.json()

        return func(*args, req_header=req_header, user=user, **kwargs)

    return wrapper


def get_json_token() -> str:
    """Loads an access token from file storage, with the 'TOKEN' .env variables.
    If no cached file is present it will create a new one. Returns an access
    token."""
    token_filepath = current_app.config["ADMIN_TOKEN_FILEPATH"]

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


def update_json_token(token_filepath):
    """Creates brand new data for token storage and persists it."""
    expiry = int(datetime.now().timestamp()) + 3600
    refresh_token = current_app.config["ADMIN_REFRESH_TOKEN"]
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
