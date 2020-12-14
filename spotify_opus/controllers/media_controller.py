import requests
from flask import Blueprint, render_template, redirect, url_for, session

from spotify_opus.models.viewmodels import CategoryResultVM, SearchItemVM

media = Blueprint("media", __name__)


@media.route("/")
def home_page():
    if 'token' not in session:
        return redirect(url_for("auth.log_in"))

    token = session["token"]
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get("https://api.spotify.com/v1/me", headers=headers)

    if response.status_code != 200:
        return redirect(url_for("auth.log_in"))

    username = response.json()["display_name"]




    results = []

    return render_template("media.html", results=results, username=username, navbar=True)
