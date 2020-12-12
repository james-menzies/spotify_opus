from typing import List
from flask import Blueprint

from spotify_opus.controllers.auth_controller import auth
from spotify_opus.controllers.media_controller import media
from spotify_opus.controllers.work_controller import works

registerable_controllers: List[Blueprint] = [
    media,
    works,
    auth,
]
