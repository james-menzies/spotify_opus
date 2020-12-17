import logging
from typing import Tuple, List, Optional

import requests
from flask import current_app
from sqlalchemy.orm import aliased
from werkzeug.exceptions import NotFound

from spotify_opus import db
from spotify_opus.models.Album import Album
from spotify_opus.models.Artist import Artist
from spotify_opus.models.Composer import Composer
from spotify_opus.services.oauth_service import verify_user

album_params = {
    "limit": 50
}

@verify_user
def extract_data(composer_id: int, user, req_header):
    try:
        c = aliased(Composer)
        query = db.session.query(Artist)
        query = query.join(c, Artist.composer)
        query = query.filter(c.composer_id == composer_id)
        query_id = query.one().external_id

    except NotFound:
        print("Composer ID does not exist in database.")
        return

    albums: List[Album] = []

    url = f"https://api.spotify.com/v1/artists/{query_id}/albums"
    extraction_complete = False
    while not extraction_complete:

        batch, next_url = get_album_batch(url, req_header)

        if next_url:
            url = next_url
        else:
            extraction_complete = True

        albums += batch
        current_app.logger.info("Batch of albums processed")

    size = len(albums)
    for index, album in enumerate(albums):





    db.session.add_all(albums)
    db.session.commit()


def get_album_batch(url: str, req_header: dict) -> Tuple[List[Album], Optional[str]]:
    """Returns a batch of albums as well as a url string for the next
    retrieval of items. If this was the last page, the second item in
    the returned Tuple with be None"""
    response = requests.get(url, headers=req_header, params=album_params)
    data = response.json()
    album_items_data = data["items"]
    next_url = data["next"]

    return [create_album(item) for item in album_items_data], next_url


def create_album(album_data: dict) -> Album:
    album = Album()
    album.name = album_data["name"]
    album.external_id = album_data["id"]
    album.image_url = album_data["images"][1]["url"]
    album.album_type = album_data["album_type"]
    album.release_date = album_data["release_date"]

    precision = album_data["release_date_precision"]
    if precision == "year":
        album.release_date += "-01-01"
    elif precision == "month":
        album.release_date += "-01"

    return album
