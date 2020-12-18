from spotify_opus import db


class SubSection(db.Model):
    __tablename__ = "sub_sections"

    subsection_id = db.Column(db.Integer, primary_key=True)

    work_id = db.Column(db.Integer, db.ForeignKey(
        "works.work_id"), nullable=False)

    section_number = db.Column(db.Integer, nullable=True)
