from enum import Enum

from spotify_opus import db
from spotify_opus.models.WorkComponent import WorkComponent


class Genre(Enum):
    symphony = 1
    concerto = 2
    opera = 3
    ballet = 4
    chamber = 5
    other = 6


class Work(WorkComponent):
    __tablename__ = "works"

    work_id = db.Column(db.Integer, db.ForeignKey(
        "work_components.component_id"), primary_key=True)

    date_written = db.Column(db.Date, nullable=False)
    genre = db.Column(db.Enum(Genre), nullable=False)
    genre_ordinal = db.Column(db.Integer, nullable=True)
    subtitle = db.Column(db.String(), nullable=True)
    more_info = db.Column(db.String(), nullable=True)
    catalog_no = db.Column(db.String(), nullable=True)
    opus_no = db.Column(db.String(), nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "work"
    }
