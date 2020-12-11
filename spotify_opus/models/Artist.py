from sqlalchemy import Column, String

from spotify_opus.models.ContextObject import ContextObject


class Artist(ContextObject):

    __tablename__ = "artists"
    name = Column(String(), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "artist"
    }

