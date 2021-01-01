import re
from typing import Dict, Optional, List

from sqlalchemy.orm import contains_eager

from spotify_opus import db
from spotify_opus.models.Album import Album
from spotify_opus.models.Artist import Artist
from spotify_opus.models.Composer import Composer
from spotify_opus.models.Performance import Performance
from spotify_opus.models.Track import Track
from spotify_opus.models.Work import Work


class Generator:
    opus_ids = (
        re.compile(r"Op.\s?[\d]+[a-l]?( No.\s?[\d]+)?"),
        re.compile(r"WoO\s?[\d]+[a-l]?( No.\s?[\d]+)?")
    )
    unspaced_woo = re.compile(r"WoO\d+")

    roman_num = re.compile(r"[MDCLXVI]+\..+")

    spaced_elements = (
        re.compile(r"Op.[\s]+"),
        re.compile(r"No.[\s]+")
    )

    work_sep = re.compile(r", :")

    prefix = re.compile(r"Beethoven: ")

    def __init__(self):
        query = db.session.query(Composer)
        query = query.filter(Composer.name == "Ludwig van Beethoven")
        self.composer: Composer = query.first_or_404()
        self.performances: List[Performance] = []
        self.works: Dict[str, Work] = {}

    def generate_works_from_tracks(self):

        query = db.session.query(Album)
        query = query.join(Album.tracks)
        query = query.options(contains_eager(Album.tracks))
        query = query.join(Track.artists)
        query = query.join(Artist.composer)
        query = query.filter(Composer.composer_id == self.composer.composer_id)

        albums = query.all()
        for album in albums:

            new_performances: Dict[Work, Performance] = {}
            for track in album.tracks:

                work = self.process_track(track)
                if work:
                    if work.opus_no not in self.works:
                        self.works[work.opus_no] = work
                    else:
                        work = self.works[work.opus_no]

                    if work not in new_performances:
                        performance = Performance()
                        performance.work = work
                        performance.album = album
                        new_performances[work] = performance

                    new_performances[work].tracks.append(track)

        db.session.add_all(self.works.values())
        db.session.commit()

    def process_track(self, track: Track) -> Optional[Work]:
        """Sanitizes the name of a track, then creates a Work object
        based off the track name and returns it."""

        track_name: str = track.name
        if re.match(self.prefix, track_name):
            track_name = track_name.replace("Beethoven: ", "")

        matches = [re.search(pattern, track.name) for pattern in self.opus_ids]
        matches = [match.group() for match in matches if match]

        if not matches:
            return None

        opus_no = matches[0]
        track_name = track_name.replace(opus_no, "")
        opus_no = opus_no.replace("Op. ", "Op.")
        opus_no = opus_no.replace("No. ", "No.")

        if re.search(self.unspaced_woo, opus_no):
            opus_no = opus_no.replace("WoO", "WoO ")

        roman_suffix = re.search(self.roman_num, track_name)

        if re.search(self.work_sep, track_name):
            work_name, *sanitized_name = re.split(self.work_sep, track_name)
        elif ":" in track_name:
            return None
        elif roman_suffix:
            substring = roman_suffix.group()
            sanitized_name = substring
            work_name = track_name.replace(substring, "")
        else:
            work_name = sanitized_name = track_name

        if isinstance(sanitized_name, list):
            sanitized_name = "".join(sanitized_name)

        sanitized_name = self.reformat_attribute(sanitized_name)
        work_name = self.reformat_attribute(work_name)

        track.sanitized_name = sanitized_name

        work = Work()
        work.name = work_name
        work.opus_no = opus_no
        work.composer_id = self.composer.composer_id

        return work

    def reformat_attribute(self, value: str):
        for pattern in self.spaced_elements:
            match = re.search(pattern, value)
            if match:
                value = value.replace(match.group(), match.group().strip())

        value = value.strip()
        if value[-1] == ",":
            value = value[:-1]

        return value


Generator().generate_works_from_tracks()
