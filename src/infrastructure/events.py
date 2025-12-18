from src.infrastructure.logger import logger
from random import randint

from src.events.advertisement import AdvertisementEvent
from src.events.bet import BetEvent
from src.events.geese_unite import GeeseUniteEvent
from src.events.golden_goose import GoldenGooseEvent
from src.events.goose_attack import GooseAttackEvent
from src.events.goose_steal import GooseStealEvent
from src.events.stroke import StrokeEvent


class Events:
    def __init__(self, casino):
        self._logger = logger
        self.casino = casino
        self.events = [
            ("bet", 60, BetEvent(casino).player_bet_event),
            ("goose_attack", 30, GooseAttackEvent(casino).goose_attack_event),
            ("goose_steal", 15, GooseStealEvent(casino).goose_steal_event),
            ("geese_unite", 10, GeeseUniteEvent(casino).geese_unite_event),
            ("advertisement", 30, AdvertisementEvent(casino).advertisement_event),
            ("stroke", 1000, StrokeEvent(casino).stroke_event),
            # ("golden_goose", 5, GoldenGooseEvent(casino).golden_goose_event)
        ]

    def get_random_event(self):
        '''Chose random event from the list by their weight'''
        total = sum(possibility for _, possibility, _ in self.events)
        result = randint(1, total)
        current = 0

        for name, possibility, event_class in self.events:
            current += possibility
            if result <= current:
                event_instance = event_class
                return event_instance

        # in case of exception
        return self.events[0][2]
