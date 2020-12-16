import json
import os
from datetime import datetime
from functools import wraps

import pytz
import requests
from flask import session, redirect, url_for, has_request_context


def get_json_token(filename: str):
    with open(filename, "r") as file:
        data = json.load(file)

    now = datetime.now().timestamp()
    if data["expires_at"] < now:
        expiry = datetime.now().timestamp() + 3600
        data["access_token"] = get_new_token(data["refresh_token"])
        data["expires_at"] = expiry


    with open(filename, "w") as file:
        json.dump(data, file)

    return data["access_token"]


def get_new_token(refresh_token: str):
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
    return response.json()["access_token"]


def verify_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if has_request_context() and 'token' not in session:
            return redirect(url_for("auth.log_in"))
        elif not has_request_context():
            token = get_json_token("resources/tokens/dev.json")
        else:
            token = session["token"]

        req_header = get_auth_header(token)

        response = requests.get("https://api.spotify.com/v1/me", headers=req_header)

        if response.status_code != 200:
            return redirect(url_for("auth.log_in"))

        user = response.json()

        return func(*args, req_header=req_header, user=user, **kwargs)

    return wrapper


def get_auth_header(token: str):
    return {
        "Authorization": f"Bearer {token}"
    }
