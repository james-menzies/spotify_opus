from typing import List
from flask import Blueprint

from spotify_opus.controllers.album_controller import album
from spotify_opus.controllers.auth_controller import auth
from spotify_opus.controllers.media_controller import media
from spotify_opus.controllers.composer_controller import composer

registerable_controllers: List[Blueprint] = [
    media,
    composer,
    auth,
    album,
]
