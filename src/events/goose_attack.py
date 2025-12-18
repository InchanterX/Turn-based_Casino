from src.infrastructure.logger import logger
from src.infrastructure.events_instruments import EventsInstruments
from src.infrastructure.goose import GoldenGoose


class GooseAttackEvent:
    '''Chose a random goose to execute its attack skill'''

    def __init__(self, casino):
        self.casino = casino
        self.instruments = EventsInstruments(casino)

    def _get_player(self):
        '''Literally get random player'''
        return self.instruments.random_player()

    def _get_goose(self):
        '''Literally get random goose'''
        return self.instruments.random_goose()

    def goose_attack_event(self):
        '''Goose attacks a player'''

        player = self._get_player()
        goose = self._get_goose()

        if player is None or goose is None:
            return "[🦢 Goose] No players or geese for attack"

        # Attack
        if isinstance(goose, GoldenGoose):
            collected = goose.attack_player(player, self.casino.geese)
            if collected > 0:
                return f"[🦢💰] {goose.name} attacked {player.name}, собрал {collected} с гусей и поделился!"
            else:
                return f"[🦢] {goose.name} attacked {player.name} but all geese are poor!"
        else:
            input(
                f"{goose.name} is going to strick {player.name}! Try to parry it by throwing a dice.\n>")
            value = player.roll_the_dice()
            goose.attack_player(player, value)
            return f"[🦢] {goose.name} атаковал {player.name} на {goose.damage} урона!"
