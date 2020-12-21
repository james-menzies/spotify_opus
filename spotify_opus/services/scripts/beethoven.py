import re

from spotify_opus import db
from spotify_opus.models.Composer import Composer
from spotify_opus.models.Track import Track
from spotify_opus.models.Work import Work


class Generator:
    opus_ids = [
        re.compile("Op.\s?[\d]*[a-l]?( No. [\d]*)?"),
        re.compile("WoO\s?[\d]*")
    ]

    work_sep = re.compile(", :")


    prefix = re.compile("Beethoven: ")

    def __init__(self):
        query = db.session.query(Composer)
        query = query.filter(Composer.name == "Ludwig van Beethoven")
        self.composer = query.first_or_404()


        self.works = set()

    def generate_works_from_tracks(self):
        query = db.session.query(Track)
        query = query.join(Track.artists)
        query = query.join(Composer)
        query = query.filter(Composer.composer_id == self.composer.composer_id)
        tracks = query.all()

        for track in tracks:

            track_name: str = track.name
            if re.match(self.prefix, track_name):
                track_name = track_name.replace("Beethoven: ", "")

            matches = [re.search(pattern, track.name) for pattern in self.opus_ids]
            matches = [match.group() for match in matches if match]

            if not matches:
                continue

            opus_no = matches[0]
            track_name = track_name.replace(opus_no, "")
            opus_no = opus_no.replace("Op. ", "Op.")
            opus_no = opus_no.replace("No. ", "No.")


            # print(f"Work: {track_name} ({opus_no})")
            if ":" in track_name:
                work_name,  *san_name = re.split(self.work_sep, track_name)
                if len(san_name) > 1:
                    san_name = san_name[1]
            else:
                work_name = san_name = track_name

            track.sanitized_name = san_name
            work = Work()
            work.name = work_name
            work.opus_no = opus_no
            work.composer_id = self.composer.composer_id
            self.works.add(work)

        db.session.bulk_save_objects(self.works)
        db.session.commit()









Generator().generate_works_from_tracks()
