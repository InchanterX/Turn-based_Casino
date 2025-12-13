from src.infrastructure.logger import logger
from src.infrastructure.chips import ChipsCollection
from src.infrastructure.effects import EffectsCollection
from src.infrastructure.constants import DEFAULT_PLAYER_HEALTH, DEFAULT_PLAYER_LUCK


class Player:
    def __init__(self, name: str, balance: int):
        self._logger = logger
        self.name = name
        self.balance = balance
        self.luck = DEFAULT_PLAYER_LUCK
        self.health = DEFAULT_PLAYER_HEALTH
        self.chips = ChipsCollection()
        self.effects = EffectsCollection()

    def get_chips_value(self):
        '''Total chips value'''
        return self.chips.total_value()

    def income(self, amount: int):
        '''Increase amount of players chips by the given number.'''
        self.balance += amount
        self.chips.add(amount)
        logger.info(f"Added {amount} to {self.name} balance")
        print(f"Added {amount} to your balance!")

    def lesion(self, amount: int):
        '''Decrease amount of players chips by the given number'''
        if self.chips.remove(amount):
            self.balance -= amount
            logger.info(f"Removed {amount} from {self.name} balance")
            print(f"Removed {amount} from your balance!")
        else:
            logger.info(
                f"{self.name} have not enough money to less it by {amount}")
            print(
                f"You can't remove {amount} chips from your balance! You have only {self.chips.total_value()}")

    def lose_health(self, loss: int):
        '''Lose health'''
        self.health -= loss
        logger.info(f"Player {self.name} lost {loss}HP.")
        print(f"You've lost {loss}HP!")

    def decrease_luck(self, loss: int):
        '''Decrease luck'''
        self.luck -= loss
        logger.info(
            f"Player {self.name} lost {loss} units of luck. Current state: {self.luck}.")
        print("You've lost some units of luck!")

    def is_alive(self) -> bool:
        return self.health > 0

    def _repr__(self) -> str:
        status = "alive" if self.health > 0 else "dead"
        chips_value = self.get_chips_value()
        return f"Player {self.name} is {status}, has {self.health}HP, {self.luck} units of luck and chips: {chips_value}"
