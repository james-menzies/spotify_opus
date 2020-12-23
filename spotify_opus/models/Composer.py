from spotify_opus import db
from spotify_opus.models.Artist import Artist
from spotify_opus.models.Work import Work


class Composer(db.Model):
    __tablename__ = "composers"
    composer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    birth_year = db.Column(db.Integer, nullable=False)
    death_year = db.Column(db.Integer, nullable=True)
    biography = db.Column(db.String(), nullable=True)
    country = db.Column(db.String(), nullable=False)
    works = db.relationship(Work, backref="composer")

    artist = db.relationship(Artist, backref="composer", uselist=False)

    def __repr__(self):
        return f"<Composer: {self.name}>"

    def __str__(self):
        return self.name
