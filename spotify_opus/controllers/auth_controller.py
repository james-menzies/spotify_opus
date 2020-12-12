from flask import Blueprint, render_template

auth = Blueprint("auth", __name__)

@auth.route("/login")
def log_in():

    return render_template("login.html")
