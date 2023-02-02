from models.mixins import IdMixIn


class Genre(IdMixIn):
    name: str

    def transform(self) -> None:
        """Just empty method to use standard pipeline"""
