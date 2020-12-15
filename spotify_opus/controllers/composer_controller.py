import requests
from flask import Blueprint, render_template, request, abort, redirect, url_for

from spotify_opus import db, SPOTIFY_BASE_URL
from spotify_opus.forms import ComposerForm
from spotify_opus.models.Artist import Artist
from spotify_opus.models.Composer import Composer
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

    return render_template('composer_edit.html', form=form)


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
