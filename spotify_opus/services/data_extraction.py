import requests
from werkzeug.exceptions import NotFound

from spotify_opus import db
from spotify_opus.models.Composer import Composer
from spotify_opus.services.oauth_service import verify_user


@verify_user
def extract_data(composer_id: int, user, req_header):
    try:
        composer = db.session.query(Composer).get_or_404(composer_id)
    except NotFound:
        print("Composer ID does not exist in database.")
        return

    external_id = composer.artist.external_id
    url = f"https://api.spotify.com/v1/artists/{external_id}/albums"
    response = requests.get(url, headers=req_header)

    print(response.json()["total"])
