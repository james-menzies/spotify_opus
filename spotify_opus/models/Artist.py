from spotify_opus import db


class Artist(db.Model):
    __tablename__ = "artists"
    artist_id = db.Column(db.String(), primary_key=True, autoincrement=False)
    image_url = db.Column(db.String(), nullable=True)
    name = db.Column(db.String(), nullable=False)

    composer_id = db.Column(db.Integer, db.ForeignKey(
        "composers.composer_id"), nullable=True)

    def __repr__(self) -> str:
        return f"<Artist: {self.name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Artist):
            return False

        return self.artist_id == other.artist_id

    def __hash__(self):
        return hash(self.artist_id)
