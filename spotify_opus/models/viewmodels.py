from typing import List


class AlbumVM:

    def __init__(self, name):
        self.name: str = name
        self.artists: List[str] = []
        self.tracks: List[TrackVM] = []
        self.image_url = ""


class TrackVM:

    def __init__(self, name: str, track_number: int):
        self.name: str = name
        self.track_number: int = track_number

    def __repr__(self):
        return f"<TrackVM: {self.track_number}: {self.name}"
