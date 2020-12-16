from typing import Callable

import requests
from flask import Blueprint, render_template, request, url_for

from spotify_opus import SPOTIFY_BASE_URL
from spotify_opus.models.viewmodels import CategoryResultVM, SearchItemVM
from spotify_opus.services.oauth_service import verify_user

media = Blueprint("media", __name__)


@media.route("/")
@verify_user
def home_page(user, req_header):
    results = None
    username = user["display_name"]
    limit = 3
    item_type = "artist,album,track"
    offset = 0

    if "type" in request.args:
        requested_types = request.args["type"].split(",")
        if len(requested_types) == 1:
            limit = 15

    if "page" in request.args:
        page_num = int(request.args["page"])
        offset = limit * (page_num - 1)
        offset = str(offset)

    if "q" in request.args:
        search_data = get_search_results(
            request.args["q"], req_header, item_type, limit, offset)
        results = process_spotify_json(search_data)

    return render_template(
        "media.html", results=results, username=username, navbar=True)


def get_search_results(query, req_header, item_type, limit=3, offset=0):
    params = {
        "q": query,
        "type": item_type,
        "limit": limit,
        "offset": offset,
    }

    response = requests.get(f"{SPOTIFY_BASE_URL}/v1/search",
                            params=params, headers=req_header)

    if response.status_code != 200:
        raise ValueError("Error on server side when retrieving search results")

    return response.json()


def process_spotify_json(search_data: dict):
    results = []

    def gen_section(key: str, func: Callable[[dict], SearchItemVM]) -> None:
        if key not in search_data:
            return

        section = CategoryResultVM(key.capitalize())
        for item in search_data[key]["items"]:
            result = func(item)
            section.items.append(result)

        results.append(section)

    gen_section("albums", lambda album: SearchItemVM(
        url=url_for("album.view_album", album_id=album["id"]),
        image_url=album["images"][1]["url"],
        primary_label=album["name"],
        sec_label=album["artists"][0]["name"]
    ))

    gen_section("artists", lambda artist: SearchItemVM(
        url=artist["href"],
        image_url=artist["images"][1]["url"],
        primary_label=artist["name"]
    ))

    gen_section("tracks", lambda track: SearchItemVM(
        url=url_for("album.view_album", album_id=track["album"]["id"]),
        image_url=track["album"]["images"][1]["url"],
        primary_label=track["name"],
        sec_label=track["artists"][0]["name"]
    ))

    return results
