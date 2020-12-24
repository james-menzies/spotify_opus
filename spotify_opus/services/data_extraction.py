from typing import Tuple, List, Optional, Callable, TypeVar, Set, Any

import requests
from werkzeug.exceptions import NotFound

from spotify_opus import db
from spotify_opus.models.Album import Album
from spotify_opus.models.Artist import Artist
from spotify_opus.models.Composer import Composer
from spotify_opus.models.Track import Track, association_table
from spotify_opus.services.oauth_service import VerifyUser

max_params = {
    "limit": 50
}

T = TypeVar("T")


def extract_data(composer_id: int):
    try:
        composer = db.session.query(Composer).get_or_404(composer_id)

    except NotFound:
        print("Composer ID does not exist in database.")
        return

    query_id = composer.artist.artist_id
    url = f"https://api.spotify.com/v1/artists/{query_id}/albums"
    artists: Set[Artist] = set()
    albums = extract_items(
        lambda data: create_album(data, artists), url)

    tracks = []
    url = "https://api.spotify.com/v1/albums/{}/tracks"

    existing_albums = Album.query.all()
    existing_artists = Artist.query.all()

    new_albums = [album for album in albums if album not in existing_albums]
    new_artists = {artist for artist in artists if artist not in existing_artists}

    db.session.bulk_save_objects(new_albums)
    db.session.bulk_save_objects(new_artists)
    db.session.flush()

    total_albums = len(albums)
    for item, album in enumerate(albums):
        if item % 20 == 0:
            print (f"{item}/{total_albums} albums processed")

        formatted_url = url.format(album.album_id)
        album_tracks = extract_items(
            lambda data: create_track(data, artists), formatted_url)

        for track in album_tracks:
            track.album_id = album.album_id
        tracks += album_tracks

    db.session.bulk_save_objects(tracks)

    track_artists = []
    for track in tracks:

        for artist in track.artists:
            track_artists.append({
                "track_id": track.track_id,
                "artist_id": artist.artist_id
            })

    db.session.execute(association_table.insert().values(track_artists))
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
        else:
            extraction_complete = True
        items += batch

    return items


@VerifyUser
def get_batch(url: str, create_func, req_header: dict,
              user) -> Tuple[List[Any], Optional[str]]:
    """Returns a batch of items as well as a url string for the next
    retrieval of items. If this was the last page, the second item in
    the returned Tuple will be None"""
    response = requests.get(url, headers=req_header, params=max_params)
    data = response.json()
    items_data = data["items"]
    next_url = data["next"]

    return [create_func(item) for item in items_data], next_url


def create_album(album_data: dict, artists: Set[Artist]) -> Album:
    album = Album()
    album.name = album_data["name"]
    album.album_id = album_data["id"]
    album.image_url = album_data["images"][1]["url"]
    album.album_type = album_data["album_type"]
    album.release_date = album_data["release_date"]

    album_artists = album_data["artists"]
    new_artists = {create_artist(album_artist) for album_artist in album_artists}
    artists.update(new_artists)

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
    track.name = track_data["name"]
    track.track_id = track_data["id"]
    track.track_number = track_data["track_number"]
    track.duration_ms = track_data["duration_ms"]
    track.disc_no = track_data["disc_number"]
    track.explicit = track_data["explicit"]
    artist_ids = [a["id"] for a in track_data["artists"]]
    track.artists = [artist for artist in artists if artist.artist_id in artist_ids]
    return track


def create_artist(artist_data: str) -> Artist:
    artist = Artist()
    artist.name = artist_data["name"]
    artist.artist_id = artist_data["id"]
    return artist
