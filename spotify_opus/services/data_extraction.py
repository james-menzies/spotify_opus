from werkzeug.exceptions import NotFound

from spotify_opus import db
from spotify_opus.models.Composer import Composer
from spotify_opus.services.oauth_service import VerifyUser


@VerifyUser(client_credentials=True)
def extract_data(composer_id: int, req_header):
    try:
        composer = db.session.query(Composer).get(composer_id)

    except NotFound:
        print("Composer ID does not exist in database.")
        return

    external_id = composer.artist.external_id
