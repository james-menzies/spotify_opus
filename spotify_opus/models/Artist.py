from sqlalchemy import Column, String, ForeignKey

from spotify_opus import db
from spotify_opus.models.ContextObject import ContextObject


class Artist(ContextObject):

    __tablename__ = "artists"
    artist_id = db.Column(db.Integer(), ForeignKey(
        "context_objects.context_id"), primary_key=True)


    __mapper_args__ = {
        "polymorphic_identity": "artist"
    }

