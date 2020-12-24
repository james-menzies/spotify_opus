from spotify_opus import db
from spotify_opus.models.Artist import Artist
from spotify_opus.models.Work import Work


class Composer(db.Model):
    __tablename__ = "composers"

    composer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False,
                     info={"label": "Name"})
    birth_year = db.Column(db.Integer, nullable=False,
                           info={"label": "Year of Birth"})

    death_year = db.Column(db.Integer, nullable=True,
                           info={"label": "Year of Death"})

    country = db.Column(db.String(), nullable=False,
                        info={"label": "Country of Origin"})

    biography = db.Column(db.String(), nullable=True,
                          info={"label": "Biography"})

    works = db.relationship(Work, backref="composer")

    artist = db.relationship(Artist, backref="composer", uselist=False)

    death_after = db.CheckConstraint("birth_year < death_year", name="death_after")



    def __repr__(self):
        return f"<Composer: {self.name}>"

    def __str__(self):
        return self.name
