from typing import List


class SearchItemVM:

    def __init__(self, url: str, image_url: str,
                 primary_label: str = "Result Name", sec_label: str = None):
        self.url = url
        self.image_url = image_url
        self.primary_label = primary_label
        self.sec_label = sec_label


class CategoryResultVM:

    def __init__(self, name: str):
        self.name: str = name
        self.items: List[SearchItemVM] = []
