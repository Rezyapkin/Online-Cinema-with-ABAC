from models.mixins import IdMixIn


class Person(IdMixIn):
    name: str

    def transform(self) -> None:
        """Just empty method to use standard pipeline"""
