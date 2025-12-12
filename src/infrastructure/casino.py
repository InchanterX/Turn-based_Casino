from src.infrastructure.collections import Player_Collection, Goose_Collection, Casino_Collection
from src.infrastructure.player import Player
from src.infrastructure.goose import WarGoose, HonkGoose, UnluckyGoose, GoldenGoose
from src.infrastructure.events import Events
from src.infrastructure.constants import DEFAULT_BALANCE


class Casino:
    def __init__(self):
        self.players = Player_Collection()
        self.geese = Goose_Collection()
        self.balance = Casino_Collection()
        self.events = Events(self)

    def register_default(self, user_name: str) -> None:
        # define player
        self.players.append(Player(user_name, DEFAULT_BALANCE))

        # define geese
        self.geese.append(WarGoose("Warrior"))
        self.geese.append(HonkGoose("Noise"))
        self.geese.append(UnluckyGoose("Underdog"))
        self.geese.append(GoldenGoose("Sparkle"))

    def random_event(self):
        self.events.run_random_event()
