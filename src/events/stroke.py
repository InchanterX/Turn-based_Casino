from src.infrastructure.logger import logger
from src.infrastructure.events_instruments import EventsInstruments


class StrokeEvent():
    '''Stroke the player for a lot of damage with an ability too dodge it'''

    def __init__(self, casino):
        self.casino = casino
        self.instruments = EventsInstruments(casino)

    def _get_player(self):
        '''Literally get random player'''
        return self.instruments.random_player()

    def stroke_event(self) -> bool:
        '''Hit player with stroke'''
        # print("STROKE")
        player = self._get_player()
        input(
            f"{player.name} fills a terrible pain... Try to parry it by throwing a dice.\n>")
        value = player.roll_the_dice()
        result = int(100/value)
        player.lose_health(result)
        logger.info(
            f"Player {player.name} rolled {value} and was damaged by the stroke for {result}.")
        print(
            f"[💀 Stroke] Player {player.name} rolled {value} has struck by {result} by a stroke!")
        return True
