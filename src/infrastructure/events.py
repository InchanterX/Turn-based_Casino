from src.infrastructure.logger import logger
from random import choice
from src.infrastructure.player import Player


class Events:
    def __init__(self, casino):
        self._logger = logger
        self.casino = casino

        # list of available events
        self.events = [
            self.stroke,
            self.advertisement
        ]

    def _random_player(self):
        '''
        Select random player from the list.
        In default implementation there is only one player, so it will always chose it.
        '''
        return choice(self.casino.players)

    def advertisement(self, player) -> None:
        '''Print advertisement to the CLI'''
        logger.info(
            f"Displayed advertisement to the player {player}.")
        print("Today and only today! Depni hatu v casino!")

    def stroke(self) -> None:
        player = self._random_player()
        player.lose_health(100)
        logger.info(
            f"Player {player.name} has died from the stroke.")
        print(
            f"Player {player.name} has died because of stroke! How unfortunately...")
