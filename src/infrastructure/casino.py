from src.infrastructure.collections.geese import GooseCollection
from src.infrastructure.collections.casino import CasinoCollection
from src.infrastructure.collections.players import PlayerCollection
from src.infrastructure.player import Player
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
        self.geese.append(WarGoose("Warrior"))
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

    # def geese_unite_event(self):
    #     if len(self.geese) >= 2:
    #         goose1 = choice(self.geese)
    #         goose2 = choice([goose for goose in self.geese])

    #         group = goose1 + goose2
    #         self.geese.remove(goose1)
    #         self.geese.remove(goose2)
    #         self.geese.append(group)
    #         print(f"Geese {goose1} and {goose2} gathered to group!")

    def players_status_check(self) -> bool:
        for i in range(self.players.__len__()):
            if not self.players.__getitem__(i).is_alive():
                logger.info(
                    f"Player {self.players.__getitem__(i).name} is dead.\nStopping simulation.")
                print("Stopping simulation.")
                self.players.remove(self.players.__getitem__(i))
                return True

            # debug information
            print(
                f"Name: {self.players.__getitem__(i).name},\n Balance: {self.players.__getitem__(i).balance},\n Luck: {self.players.__getitem__(i).luck},\n Health: {self.players.__getitem__(i).health}")
            print(
                f"Total chips: {self.players.__getitem__(i).get_chips_value()}, Chips list: {self.players.__getitem__(i).chips.get_info()}")
            print(
                f"Effects applied: {self.players.__getitem__(i).effects.__repr__()}")
        return False

    def make_effects_step(self):
        for i in range(self.players.__len__()):
            self.players.__getitem__(i).effects.make_step()
