from flask import Blueprint, render_template, \
    redirect, request, url_for, session

from spotify_opus.services.oauth_service import \
    process_callback, get_authorization_url

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login")
def log_in():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def authorize():
    url = get_authorization_url()

    return redirect(url)


@auth.route("/callback")
def callback():
    if "error" in request.args:
        return redirect(url_for(".log_in"))

    response = process_callback(request.args["code"])

    if response.status_code == 200:
        session.permanent = True
        data = response.json()
        session["token"] = data["access_token"]
        return redirect(url_for("composer.get_all"))


@auth.route("/logout")
def log_out():
    session.pop("token")
    return redirect(url_for(".log_in"))
