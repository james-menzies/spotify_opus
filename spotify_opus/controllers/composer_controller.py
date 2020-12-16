import requests
from flask import Blueprint, render_template, request, abort, redirect, url_for

from spotify_opus import db, SPOTIFY_BASE_URL
from spotify_opus.forms.ComposerForm import ComposerForm
from spotify_opus.models.Artist import Artist
from spotify_opus.models.Composer import Composer
from spotify_opus.models.ContextObject import ContextObject
from spotify_opus.services.oauth_service import verify_user

composer = Blueprint("composer", __name__, url_prefix="/composer")


@composer.route("/", methods=["GET"])
@verify_user
def get_all(req_header, user):
    composers = db.session.query(Composer).all()
    username = user["display_name"]
    return render_template('composer.html', composers=composers, navbar=True, username=username)


@composer.route("/create", methods=["GET"])
@verify_user
def create_new(req_header, user):
    form = ComposerForm()
    submit_url = url_for(".submit_new")
    return render_template('composer_edit.html',
                           form=form, submit_url=submit_url, navbar=True)


@composer.route("/", methods=["POST"])
@verify_user
def submit_new(req_header, user):
    form = ComposerForm(request.form)

    if not form.validate():
        return redirect(url_for("composer.create_new"))

    params = {
        "q": form.name.data,
        "type": "artist",
        "limit": 1,
    }

    response = requests.get(
        f"{SPOTIFY_BASE_URL}/v1/search", params=params, headers=req_header)

    if not response.ok:
        return abort(500, "Error in proxy search")

    artist_data = response.json()["artists"]["items"]

    if len(artist_data) == 0:
        return abort(400, "No results match against Spotify's records")

    artist_data = artist_data[0]
    artist_name = artist_data["name"]

    if artist_name.lower() != form.name.data.lower():
        return abort(400, "Name submitted does not match records")

    artist = Artist()
    artist.name = artist_name
    artist.image_url = artist_data["images"][1]["url"]
    artist.external_id = artist_data["id"]

    composer = Composer()
    for name, value in form.data.items():
        setattr(composer, name, value)

    composer.image_url = artist.image_url
    artist.composer = composer

    db.session.add(artist)
    db.session.commit()
    return redirect(url_for("composer.get_all"))


@composer.route("/edit/<int:composer_id>")
@verify_user
def edit(req_header, user, composer_id: int):
    composer = db.session.query(Composer).get_or_404(composer_id)

    form = ComposerForm(obj=composer)
    submit_url = url_for(".confirm_edit", composer_id=composer_id)
    return render_template("composer_edit.html",
                           form=form, navbar=True, submit_url=submit_url)


@composer.route("/edit/<int:composer_id>", methods=["POST"])
@verify_user
def confirm_edit(req_header, user, composer_id):
    form = ComposerForm(request.form)

    if not form.validate():
        return redirect(url_for("composer.edit", composer_id=composer_id))

    data = form.data
    data.pop("name", None)

    query = Composer.query
    query = query.filter_by(composer_id=composer_id)
    rows_affected = query.update(data)

    if not rows_affected:
        db.session.rollback()
        return abort(404, "Composer object not found")
    elif rows_affected > 1:
        db.session.rollback()
        return abort(500, "Multiple row update attempted. Aborting.")
    else:
        db.session.commit()
        return redirect(url_for(".get_all"))









