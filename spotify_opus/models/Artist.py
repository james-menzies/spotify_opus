from sqlalchemy import Column, String, ForeignKey

from spotify_opus import db
from spotify_opus.models.ContextObject import ContextObject


class Artist(ContextObject):

    __tablename__ = "artists"
    context_id = db.Column(db.Integer(), ForeignKey(
        "context_objects.context_id"), primary_key=True)
    external_id = db.Column(db.String(), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "artist"
    }

