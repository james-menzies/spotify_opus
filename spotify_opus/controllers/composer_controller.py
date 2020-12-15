from flask import Blueprint, render_template

from spotify_opus.forms import ComposerForm

composer = Blueprint("composer", __name__, url_prefix="/composer")


@composer.route("/", methods=["GET"])
def get_all_works():
    return "yo?"


@composer.route("/create", methods=["GET"])
def create_new_work():
    form = ComposerForm()

    return render_template('login.html', form=form)
