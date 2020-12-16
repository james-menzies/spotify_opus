import os
from datetime import datetime

import pytz
import requests
from flask import Blueprint, render_template, redirect, request, url_for, session, g, current_app
from requests import Request

from spotify_opus import create_app

auth = Blueprint("auth", __name__, url_prefix="/auth")
SPOTIFY_BASE_AUTH_URL = 'https://accounts.spotify.com'


@auth.route("/login")
def log_in():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def authorize():
    params = {
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "response_type": "code",
        "redirect_uri": "https://127.0.0.1:5000/auth/callback"
    }
    url = Request("GET", f"{SPOTIFY_BASE_AUTH_URL}/authorize", params=params).prepare().url
    return redirect(url)


@auth.route("/callback")
def callback():
    if "error" in request.args:
        return redirect(url_for(".log_in"))

    code = request.args["code"]
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "https://127.0.0.1:5000/auth/callback",
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET")
    }

    expiry_time = datetime.now().timestamp()

    response = requests.post(f"{SPOTIFY_BASE_AUTH_URL}/api/token", data=data, headers=headers)

    if response.status_code == 200:
        session.permanent = True
        data = response.json()
        data["expires_at"] = expiry_time

        session["token"] = data["access_token"]
        print(data)
        return redirect(url_for("media.home_page"))


@auth.route("/logout")
def log_out():
    session.pop("token")
    return redirect(url_for(".log_in"))


