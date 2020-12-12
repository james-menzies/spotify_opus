from spotify_opus import db
from spotify_opus.models.ContextObject import ContextObject


class SubSection(ContextObject):

    __tablename__ = "subsections"

    subsection_id = db.Column(db.Integer, db.ForeignKey(
        "context_objects.context_id"), primary_key=True)

    parent_id = db.Column(db.Integer, db.ForeignKey(
        "works.work_id"), nullable=False)

    number_in_parent = db.Column(db.Integer, nullable=True)
