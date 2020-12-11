from flask import Blueprint
from spotify_opus.models.ContextObject import ContextObject
from spotify_opus.models.Artist import Artist

search = Blueprint("search", "spotify_opus", url_prefix="/search")
