import requests
from flask import Blueprint, render_template, request, abort, redirect, url_for, flash

from spotify_opus import db, SPOTIFY_BASE_URL
from spotify_opus.forms.ComposerForm import ComposerForm
from spotify_opus.models.Artist import Artist
from spotify_opus.models.Composer import Composer
from spotify_opus.models.Work import Work
from spotify_opus.services.oauth_service import VerifyUser

composer = Blueprint("composer", __name__)


@composer.route("/", methods=["GET"])
@VerifyUser()
def get_all(req_header, user, success=None):
    composers = db.session.query(Composer).all()
    return render_template('composer.jinja2', composers=composers,
                           navbar=True, user=user, success=success)


@composer.route("/create", methods=["GET"])
@VerifyUser(admin=True)
def create_new(req_header, user):
    form = ComposerForm()
    submit_url = url_for(".submit_new")
    return render_template('composer_edit.jinja2',
                           form=form, submit_url=submit_url,
                           navbar=True, user=user)


@composer.route("/", methods=["POST"])
@VerifyUser(admin=True)
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
        flash("Composer name does not match the name of a Spotify artist", "danger")
        return redirect(url_for(".get_all"))

    artist_data = artist_data[0]
    artist = create_artist(artist_data)

    if artist.name.lower() != form.name.data.lower():
        flash("Name submitted does not match records", "danger")
        return redirect(url_for(".get_all"))

    existing_artist = db.session.query(Artist).get(artist.artist_id)

    if existing_artist:
        artist = existing_artist

    composer = Composer()
    for name, value in form.data.items():
        setattr(composer, name, value)

    composer.image_url = artist.image_url
    artist.composer = composer

    db.session.add(artist)
    db.session.commit()
    flash("Composer added to database", "success")
    return redirect(url_for("composer.get_all"))


def create_artist(artist_data: dict) -> Artist:
    """Creates a native Artist object from a raw Spotify artist object."""
    artist = Artist()
    artist.name = artist_data["name"]
    artist.image_url = artist_data["images"][1]["url"]
    artist.artist_id = artist_data["id"]

    return artist


@composer.route("/edit/<int:composer_id>")
@VerifyUser(admin=True)
def edit(req_header, user, composer_id: int):
    composer = db.session.query(Composer).get_or_404(composer_id)

    form = ComposerForm(obj=composer)
    submit_url = url_for(".confirm_edit", composer_id=composer_id)
    delete_url = url_for(".delete", composer_id=composer_id)

    return render_template("composer_edit.jinja2",
                           form=form, navbar=True,
                           submit_url=submit_url, delete_url=delete_url,
                           user=user)


@composer.route("/edit/<int:composer_id>", methods=["POST"])
@VerifyUser(admin=True)
def confirm_edit(req_header, user, composer_id):
    form = ComposerForm(request.form)

    if not form.validate():
        flash("Form invalid. Please check fields and retry.")
        return redirect(url_for("composer.edit", composer_id=composer_id))

    data = form.data
    data.pop("name", None)

    query = db.session.query(Composer)
    query = query.filter_by(composer_id=composer_id)
    rows_affected = query.update(data)
    return complete_update_query(rows_affected)


def complete_update_query(rows_affected: int):
    if not rows_affected:
        db.session.rollback()
        flash("Composer object not found", "danger")
    elif rows_affected > 1:
        db.session.rollback()
        flash("Server error when updating composer", "danger")
    else:
        db.session.commit()
        flash(f"Composer successfully updated.", "success")

    return redirect(url_for(".get_all"))


@composer.route("/delete/<int:composer_id>", methods=["POST"])
@VerifyUser()
def delete(req_header, user, composer_id):
    query = db.session.query(Composer)
    query = query.filter(Composer.composer_id == composer_id)
    composer = query.first()

    query = query.join(Work)
    composer_with_works = query.first()

    if composer and not composer_with_works:
        db.session.delete(composer)

        query = db.session.query(Artist)
        query = query.filter(Artist.composer_id == composer_id)
        query.update({Artist.composer_id: None})
        db.session.commit()
        flash("Composer successfully deleted.", "success")
    elif composer_with_works:
        flash("Composer has works associated, cannot delete until works are manually removed.", "danger")
    else:
        flash("Composer does not exist.", "danger")

    return redirect(url_for(".get_all"))
