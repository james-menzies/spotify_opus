from typing import Tuple, List, Optional, Callable, TypeVar, Set

import requests
from sqlalchemy.orm import aliased
from werkzeug.exceptions import NotFound

from spotify_opus import db
from spotify_opus.models.Album import Album
from spotify_opus.models.Artist import Artist
from spotify_opus.models.Composer import Composer
from spotify_opus.models.ContextObject import ContextObject
from spotify_opus.models.Track import Track
from spotify_opus.services.oauth_service import verify_user

max_params = {
    "limit": 50
}

T = TypeVar("T")


def extract_data(composer_id: int):
    try:
        composer = db.session.query(Composer).get(composer_id)

    except NotFound:
        print("Composer ID does not exist in database.")
        return

    external_id = composer.artist.external_id
    url = f"https://api.spotify.com/v1/artists/{query_id}/albums"
    albums = extract_items(create_album, url)

    tracks = []
    url = "https://api.spotify.com/v1/albums/{}/tracks"

    db.session.add_all(albums)
    db.session.commit()

    for album in albums:
        formatted_url = url.format(album.external_id)
        album_tracks = extract_items(create_track, formatted_url)
        for track in album_tracks:
            track.album_id = album.album_id
        tracks += album_tracks

    db.session.add_all(tracks)
    db.session.commit()


def extract_items(create_func: Callable, url: str) -> List[T]:
    """A generic function to take all items from a Spotify
    paging object."""
    items: List[T] = []
    extraction_complete = False
    while not extraction_complete:

        batch, next_url = get_batch(url, create_func)
        if next_url:
            url = next_url

        extraction_complete = True
        items += batch

    return items


@verify_user
def get_batch(url: str, create_func, req_header: dict,
              user) -> Tuple[List[Album], Optional[str]]:
    """Returns a batch of items as well as a url string for the next
    retrieval of items. If this was the last page, the second item in
    the returned Tuple will be None"""
    response = requests.get(url, headers=req_header, params=max_params)
    data = response.json()
    items_data = data["items"]
    next_url = data["next"]

    return [create_func(item) for item in items_data], next_url


def add_super_attributes(obj: ContextObject, data):
    obj.name = data["name"]
    obj.external_id = data["id"]
    obj.image_url = data["album"]["images"][1]["url"]


def create_album(album_data: dict) -> Album:
    album = Album()
    add_super_attributes(album, album_data)
    album.album_type = album_data["album_type"]
    album.release_date = album_data["release_date"]

    precision = album_data["release_date_precision"]
    if precision == "year":
        album.release_date += "-01-01"
    elif precision == "month":
        album.release_date += "-01"

    return album


def create_track(
        track_data: dict, artists: Set[Artist] = None) -> Track:
    """Processes a raw Spotify track object and converts
    it to a native ORM model. It will also append any artists
    found if a set is provided."""

    track = Track()
    add_super_attributes(track, track_data)
    track.duration_ms = track_data["duration_ms"]
    track.disc_no = track_data["disc_number"]
    track.explicit = track_data["explicit"]

    return track


def create_artist(artist_data: dict) -> Artist:
    artist = Artist()
    add_super_attributes(artist, artist_data)

