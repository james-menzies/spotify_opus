from spotify_opus import db


class Composer(db.Model):
    __tablename__ = "composers"
    composer_id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        "artists.artist_id"), nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    death_year = db.Column(db.Integer, nullable=True)
    biography = db.Column(db.String(), nullable=True)
    country = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Composer: {self.name}>"

    def __str__(self):
        return self.name
