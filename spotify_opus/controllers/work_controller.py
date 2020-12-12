from flask import Blueprint, render_template

from spotify_opus.forms import WorkForm

works = Blueprint("works", __name__, url_prefix="/works")


@works.route("/", methods=["GET"])
def get_all_works():
    return "yo?"


@works.route("/create", methods=["GET"])
def create_new_work():
    form = WorkForm()

    return render_template('login.html', form=form)
