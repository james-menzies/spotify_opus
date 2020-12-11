from spotify_opus import db


class SectionName(db.Model):

    __tablename__ = "section_names"

    name_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
