from enum import Enum

from spotify_opus import db
from spotify_opus.models.ContextObject import ContextObject


class SectionName(Enum):
    movement = 1
    act = 2
    number = 3


class WorkComponent(ContextObject):
    __tablename__ = "work_components"
    component_id = db.Column(db.Integer, db.ForeignKey(
        "context_objects.context_id"), primary_key=True)
    scale = db.Column(db.String())

    __mapper_args__ = {
        "polymorphic_identity": "work_component",
        "polymorphic_on": "scale"
    }
