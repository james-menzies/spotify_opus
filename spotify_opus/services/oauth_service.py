from functools import wraps

import requests
from flask import session, redirect, url_for


def verify_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'token' not in session:
            return redirect(url_for("auth.log_in"))

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
