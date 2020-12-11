from typing import List
from flask import Blueprint

from spotify_opus.controllers.search_controller import search

registerable_controllers: List[Blueprint] = [
    search,
]
