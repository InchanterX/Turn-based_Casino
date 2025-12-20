from src.infrastructure.collections.geese import GooseCollection
from src.infrastructure.collections.casino import CasinoCollection
from src.infrastructure.collections.players import PlayerCollection
from src.infrastructure.player import Player
from src.infrastructure.goose import Goose
from src.infrastructure.goose import WarGoose, HonkGoose, UnluckyGoose, GoldenGoose
from src.infrastructure.events import Events
from src.infrastructure.logger import logger
from src.infrastructure.constants import DEFAULT_BALANCE


class Casino:
    def __init__(self):
        self.players = PlayerCollection()
        self.geese = GooseCollection()
        self.balance = CasinoCollection()
        self.event_system = Events(self)

    def register_default(self, user_name: str) -> None:
        # define player
        self.players.append(Player(user_name, DEFAULT_BALANCE))

        # define geese
        self.geese.append(Goose("Goose"))
        self.geese.append(WarGoose("Warrior1"))
        self.geese.append(WarGoose("Warrior2"))
        self.geese.append(HonkGoose("Noise"))
        self.geese.append(UnluckyGoose("Underdog"))
        self.geese.append(GoldenGoose("Sparkle"))

    def random_event(self, step_number):
        event_function = self.event_system.get_random_event()
        result = event_function()
        logger.info(f"Event executed with a result: {result}")
        if result:
            pass
        else:
            print(f"({step_number + 1})[Event]: {result}")

    def geese_status_check(self) -> bool:
        for goose in self.geese:
            if not goose.is_alive():
                logger.info(
                    f"Goose {goose.name} is dead.")
                self.geese.remove(goose)

        return True

    def players_status_check(self) -> bool:
        for i in range(len(self.players)):
            if not self.players[i].is_alive():
                logger.info(
                    f"Player {self.players[i].name} is dead.\nStopping simulation.")
                print("Stopping simulation.")
                self.players.remove(self.players[i])
                return True

            print(
                f"Your balance: {self.players[i].balance}, Luck: {self.players[i].luck}, Health: {self.players[i].health}")
            # debug information
            # print(
            #     f"Name: {self.players[i].name},\n Balance: {self.players[i].balance},\n Luck: {self.players[i].luck},\n Health: {self.players[i].health}")
            # print(
            #     f"Total chips: {self.players[i].get_chips_value()}, Chips list: {self.players[i].chips.get_info()}")
            # print(
            #     f"Effects applied: {self.players[i].effects.__repr__()}")
            # print("----------------------------------")
            # for goose in self.geese:
            #     if isinstance(goose, GooseGroup):
            #         print(
            #             f"Moniker: {goose.name}, health: {goose.total_health}, damage: {goose.total_damage}, total_balance: {goose.total_balance}, alive_balance: {goose.total_alive_balance}, steal: {goose.steal_amount}, alive: {goose.alive_geese}")
            #     else:
            #         print(
            #             f"Moniker: {goose.name}, health: {goose.health}, damage: {goose.damage}, balance: {goose.balance}, steal: {goose.steal_amount}")
            # print("----------------------------------")
        return False

    def make_effects_step(self):
        for i in range(len(self.players)):
            self.players[i].effects.make_step()

    def proceed(self):
        input("Proceed? ")
