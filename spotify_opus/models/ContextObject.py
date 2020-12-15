from spotify_opus import db


class ContextObject(db.Model):
    __tablename__ = "context_objects"
    context_id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(), nullable=True)
    type = db.Column(db.String())
    name = db.Column(db.String(), nullable=False)

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "context_objects",
    }
