from spotify_opus import db


class ContextObject(db.Model):
    __tablename__ = "context_objects"
    context_id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(), unique=True, nullable=False)
    external_uri = db.Column(db.String(), unique=True, nullable=False)
    type = db.Column(db.String())

    __mapper_args__ = {
        "polymorphic_identity": "context_type",
        "polymorphic_on": type
    }
