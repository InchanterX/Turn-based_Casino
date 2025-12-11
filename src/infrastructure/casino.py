from src.infrastructure.collections import Player_Collection, Goose_Collection, Casino_Collection


class Casino:
    def __init__(self):
        self.players = Player_Collection()
        self.geese = Goose_Collection()
        self.balance = Casino_Collection()

    def _events(self):
        ...

    def random_event(self):
        ...
