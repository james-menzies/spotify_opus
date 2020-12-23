from spotify_opus import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<User: {self.name} ({self.email})>"
