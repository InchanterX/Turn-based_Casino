from random import choice
from src.infrastructure.logger import logger
from src.infrastructure.goose import GoldenGoose
from src.infrastructure.events_instruments import EventsInstruments


class GoldenGooseEvent:
    def __init__(self, casino):
        self.casino = casino
        self.instruments = EventsInstruments(casino)

    def _get_player(self):
        '''Literally get random player'''
        return self.instruments.random_player()

    def golden_goose_event(self) -> str:
        '''Golden goose gives bonus money to player by steeling them from other'''
        player = self._get_player()

        golden_geese = [
            goose for goose in self.casino.geese
            if isinstance(goose, GoldenGoose)
        ]

        # Create one
        if not golden_geese:
            golden_goose = GoldenGoose("Lucky One")
            self.casino.geese.append(golden_goose)
            logger.info(f"Created new GoldenGoose: {golden_goose.name}")
            return f"[💰 Golden One]: A new Golden Goose '{golden_goose.name}' appeared!"

        # Choose player
        if player is None:
            return "[💰 Golden One] No players for golden goose bonus"

        # Choose goose
        golden_goose = choice(golden_geese)

        # Calculating bonus
        if golden_goose.balance > 0:
            bonus = golden_goose.balance // 2
            golden_goose.balance -= bonus
            player.income(bonus)
            logger.info(
                f"Golden goose {golden_goose.name} gave {bonus} to {player.name}")
            return f"[💰 Golden Gift]: {golden_goose.name} gave {bonus} to {player.name}!"
        else:
            # No money? Let's steal them
            collected = golden_goose.collect_from_geese(self.casino.geese)
            if collected > 0:
                bonus = collected // 2
                player.income(bonus)
                return f"[💰 Golden Sharing]: {golden_goose.name} collected {collected}, shared {bonus} with {player.name}!"
            else:
                return f"[💰 Golden {golden_goose.name} wanted to help but all geese are broke!"
