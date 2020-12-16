from spotify_opus import db
from spotify_opus.models.ContextObject import ContextObject
from spotify_opus.models.SubSection import SubSection


class WorkComponent(ContextObject):
    __tablename__ = "work_components"

    component_id = db.Column(db.Integer, db.ForeignKey(
        "context_objects.context_id"), primary_key=True)

    component_type = db.Column(db.String(), nullable=False)

    subsection_type = db.Column(db.String(), nullable=False)

    children = db.relationship(SubSection, backref="parent", lazy="joined")

    __mapper_args__ = {
        "polymorphic_identity": "work_component",
        "polymorphic_on": "component_type"
    }
