from src.infrastructure.logger import logger
from src.infrastructure.events_instruments import EventsInstruments


class StrokeEvent():
    def __init__(self, casino):
        self.casino = casino
        self.instruments = EventsInstruments(casino)

    def _get_player(self):
        '''Literally get random player'''
        return self.instruments.random_player()

    def stroke_event(self) -> bool:
        '''Hit player with stroke'''
        player = self._get_player()
        player.lose_health(100)
        logger.info(
            f"Player {player.name} has died from the stroke.")
        print(
            f"[💀 Stroke] Player {player.name} has died because of stroke! How unfortunately...")
        return True
