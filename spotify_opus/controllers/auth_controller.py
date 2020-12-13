from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)


@auth.route("/login")
def log_in():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def authorize():
    return "sub bro"
