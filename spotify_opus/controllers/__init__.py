from typing import List
from flask import Blueprint

from spotify_opus.controllers.auth_controller import auth
from spotify_opus.controllers.composer_controller import composer
from spotify_opus.controllers.performance_controller import performance
from spotify_opus.controllers.works_controller import work

registerable_controllers: List[Blueprint] = [
    composer,
    auth,
    work,
    performance
]
