from src.infrastructure.logger import logger
from src.infrastructure.events_instruments import EventsInstruments


class GooseAttackEvent:
    def __init__(self, casino):
        self.casino = casino
        self.instruments = EventsInstruments(casino)

    def _get_player(self):
        '''Literally get random player'''
        return self.instruments.random_player()

    def _get_goose(self):
        '''Literally get random goose'''
        return self.instruments.random_goose()

    def goose_attack_event(self) -> str:
        '''Goose attacks a player'''

        player = self._get_player()
        goose = self._get_goose()

        if player is None or goose is None:
            return "[🦢 Goose] No players or geese for attack"

        # Attack
        damage = goose.attack_player(player)

        # Stole prepare
        stolen = 0
        if hasattr(goose, 'steal_from_player'):
            stolen = goose.steal_from_player(player)

        # Golden goose case
        collected_from_geese = 0
        if hasattr(goose, 'collect_from_geese'):
            collected_from_geese = goose.collect_from_geese(
                self.casino.geese)

        message_parts = []
        message_parts.append(
            f"[🦢 Goose] {goose.name} attacked {player.name} for {damage} damage!")

        if stolen > 0:
            message_parts.append(f"stole {stolen}")

        if collected_from_geese > 0:
            message_parts.append(
                f"collected {collected_from_geese} from other geese")

        return " | ".join(message_parts)
