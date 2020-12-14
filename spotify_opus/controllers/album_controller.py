import requests
from flask import Blueprint, redirect, url_for, render_template

from spotify_opus import SPOTIFY_BASE_URL
from spotify_opus.models.viewmodels import AlbumVM, TrackVM
from spotify_opus.services.oauth_service import verify_user

album = Blueprint("album", __name__, url_prefix="/album")


@album.route("/<string:album_id>")
@verify_user
def view_album(album_id: str, req_header: dict, user: dict):
    """Returns a HTML rendered view of a spotify album that
    is classical music sensitive."""

    response = requests.get(f"{SPOTIFY_BASE_URL}/v1/albums/{album_id}", headers=req_header)

    if not response.ok:
        return redirect(url_for("media.home_page"))

    album_vm = process_spotify_json(response.json())

    return render_template("album.html", album=album_vm, navbar=True)


def process_spotify_json(results: dict):
    """Processes the results of a album GET call and then
    returns an AlbumVM object for consumption by the
    application layer."""

    album_vm = AlbumVM(results["name"])
    album_vm.artists = [artist["name"] for artist in results["artists"]]
    for track in results["tracks"]["items"]:
        album_vm.tracks.append(TrackVM(
            track.name, track.track_number
        ))

    return album_vm
