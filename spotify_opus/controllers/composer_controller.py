from flask import Blueprint, render_template, request, abort, redirect, url_for

from spotify_opus.forms import ComposerForm
from spotify_opus.services.oauth_service import verify_user

composer = Blueprint("composer", __name__, url_prefix="/composer")


@composer.route("/", methods=["GET"])
@verify_user
def get_all(req_header, user):
    return "yo?"


@composer.route("/create", methods=["GET"])
@verify_user
def create_new(req_header, user):
    form = ComposerForm()

    return render_template('composer_edit.html', form=form)


@composer.route("/", methods=["POST"])
@verify_user
def submit_new(req_header, user):
    form = ComposerForm(request.form)

    if not form.validate():
        return redirect(url_for("composer.create_new"))

    Composer
