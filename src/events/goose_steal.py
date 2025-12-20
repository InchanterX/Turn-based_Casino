from src.infrastructure.logger import logger
from src.infrastructure.events_instruments import EventsInstruments


class GooseStealEvent:
    '''Chose a random goose to execute its steal skill'''

    def __init__(self, casino):
        self.casino = casino
        self.instruments = EventsInstruments(casino)

    def _get_player(self):
        '''Literally get random player'''
        return self.instruments.random_player()

    def _get_goose(self):
        '''Literally get random goose'''
        return self.instruments.random_goose()

    def goose_steal_event(self) -> bool:
        '''Goose steals money from player'''
        # print("STEAL")
        player = self._get_player()
        goose = self._get_goose()

        if player is None or goose is None:
            logger.warning("No players or geese for stealing")
            print("[💰 Steal]: No players or geese for stealing")
            return True

        # Actually steal
        if hasattr(goose, 'steal_from_player'):
            stolen = goose.steal_from_player(player)
            if stolen > 0:
                logger.info(
                    f"Goose {goose.name} stole {stolen} from {player.name}")
                return True
            else:
                logger.info(
                    f"Goose {goose.name} failed to steal from {player.name}")
                # print(
                #     f"[💰 Steal]: {goose.name} failed to steal from {player.name}!")
                return True
        else:
            logger.warning(
                f"Goose {goose.name} doesn't know how to steal!")
            print(f"[💰 Steal]: {goose.name} doesn't know how to steal!")
            return True
