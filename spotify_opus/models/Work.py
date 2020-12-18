from spotify_opus import db


class Work(db.Model):
    __tablename__ = "works"

    work_id = db.Column(db.Integer, primary_key=True)

    date_written = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(), nullable=False)
    work_number = db.Column(db.Integer, nullable=True)
    subtitle = db.Column(db.String(), nullable=True)
    more_info = db.Column(db.String(), nullable=True)
    catalog_no = db.Column(db.String(), nullable=True)
    opus_no = db.Column(db.String(), nullable=True)
