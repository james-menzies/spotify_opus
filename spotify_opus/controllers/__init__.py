from typing import List
from flask import Blueprint

from spotify_opus.controllers.auth_controller import auth
from spotify_opus.controllers.composer_controller import composer

registerable_controllers: List[Blueprint] = [
    composer,
    auth,
]
