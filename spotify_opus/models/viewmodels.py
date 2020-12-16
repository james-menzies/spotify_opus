from typing import List


class SearchItemVM:

    def __init__(self, url: str, image_url: str,
                 primary_label: str = "Result Name", sec_label: str = None):
        self.url = url
        self.image_url = image_url
        self.primary_label = primary_label
        self.sec_label = sec_label

    def __repr__(self):
        return f"<SearchItemVM: {self.primary_label}>"


class CategoryResultVM:

    def __init__(self, name: str):
        self.name: str = name
        self.items: List[SearchItemVM] = []

    def __repr__(self):
        return f"<CategoryResultVM {self.name}>"


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
        self.work_header: str = ""
        self.section_header: str = ""

    def __repr__(self):
        return f"<TrackVM: {self.track_number}: {self.name}"

