from typing import List
from flask import Blueprint

from spotify_opus.controllers.search_controller import search
from spotify_opus.controllers.work_controller import works

registerable_controllers: List[Blueprint] = [
    search,
    works,
]
