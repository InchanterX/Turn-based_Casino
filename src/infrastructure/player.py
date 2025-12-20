from random import randint
from src.infrastructure.logger import logger
from src.infrastructure.collections.chips import ChipsCollection
from src.infrastructure.collections.effects import EffectsCollection
from src.infrastructure.collections.inventories import InventoryCollection
from src.infrastructure.constants import DEFAULT_PLAYER_HEALTH, DEFAULT_PLAYER_LUCK


class Player:
    def __init__(self, name: str, balance: int):
        self._logger = logger
        self.name = name
        self.balance = balance
        self.luck = DEFAULT_PLAYER_LUCK
        self.health = DEFAULT_PLAYER_HEALTH
        self.chips = ChipsCollection()
        self.effects = EffectsCollection(self)
        self.inventory = InventoryCollection()

    def get_chips_value(self):
        '''Total chips value'''
        return self.chips.total_value()

    def balance_income(self, amount: int):
        '''Increase amount of players money by the given number.'''
        self.balance += amount
        logger.info(f"Added {amount} to {self.name} balance")
        print(f"[💰]: Added {amount} to {self.name} balance!")

    def balance_lesion(self, amount: int):
        '''Decrease amount of players money by the given number.'''
        self.balance = max(0, self.balance - amount)
        logger.info(f"Removed {amount} from {self.name} balance")
        # print(f"Removed {amount} from {self.name} balance!")

    def chips_income(self, amount: int):
        '''Increase amount of players chips by the given number.'''
        self.chips.add(amount)
        logger.info(f"Added {amount} to {self.name} balance")
        print(f"[💰]: Added {amount} to your balance!")

    def chips_lesion(self, amount: int):
        '''Decrease amount of players chips by the given number'''
        self.chips.remove(amount)
        logger.info(
            f"{self.name} have not enough money to less it by {amount}")

    def lose_health(self, loss: int):
        '''Lose health'''
        self.health -= loss
        logger.info(f"Player {self.name} lost {loss}HP.")

    def increase_health(self, gain: int):
        '''Lose health'''
        self.health += gain
        logger.info(f"Player {self.name} lost {gain}HP.")

    def decrease_luck(self, loss: int):
        '''Decrease luck'''
        self.luck -= loss
        logger.info(
            f"Player {self.name} lost {loss} units of luck. Current state: {self.luck}.")

    def increase_luck(self, gain: int):
        '''Increase luck'''
        self.luck += gain
        logger.info(
            f"Player {self.name} lost {gain} units of luck. Current state: {self.luck}.")

    def roll_the_dice(self) -> int:
        '''Return value of dice roll from 1 to 6'''
        result = randint(1, 6)
        logger.info(f"Player {self.name} rolled {result}.")
        print(f"[🎲] You rolled {result}!")
        return result

    def is_alive(self) -> bool:
        '''Return players state: True/False - Alive or Not'''
        return self.health > 0

    def _repr__(self) -> str:
        status = "alive" if self.health > 0 else "dead"
        chips_value = self.get_chips_value()
        return f"Player {self.name} is {status}, has {self.health}HP, {self.luck} units of luck and chips: {chips_value}"
