from src.infrastructure.logger import logger
from src.infrastructure.constants import DENOMINATIONS


class Chip:
    '''A class that represents one chip type'''

    def __init__(self, denomination: int, quantity: int = 0):
        self._logger = logger
        if denomination not in DENOMINATIONS:
            logger.exception(f"Invalid denomination {denomination} was given.")
            raise ValueError(f"Invalid denomination {denomination} was given!")

        self._denomination = denomination
        self._quantity = quantity

    def __add__(self, other):
        '''Add chips of the same denomination'''
        if isinstance(other, Chip) and self._denomination == other.denomination:
            return Chip(self._denomination, self._quantity + other.quantity)
        return NotImplemented

    def __sub__(self, other):
        '''Subtract chips of the same type'''
        if isinstance(other, Chip) and self._denomination == other.denomination:
            new_quantity = self._quantity - other.quantity
            if new_quantity < 0:
                new_quantity = 0
            return Chip(self._denomination, new_quantity)
        return NotImplemented

    # def _list_available_chips(self) -> str:
    #     '''Return available chips'''
    #     available_chips = ', '.join(str(key) for key in self.chips.keys())
    #     return available_chips

    def __repr__(self) -> str:
        return f"Chip({self._denomination}: {self._quantity})"

    def chip_total_value(self):
        '''Return total price of the denomination chips'''
        return self._denomination * self._quantity


class ChipsCollection:
    '''Collection of all players chips'''

    def __init__(self, initial_balance: int = 0):
        '''Creating chips of all denominations'''
        self._logger = logger
        self.chips = {
            1: Chip(1, 0),
            5: Chip(5, 0),
            25: Chip(25, 0),
            100: Chip(100, 0),
        }

        if initial_balance > 0:
            self._add_money(initial_balance)

    def _add_money(self, amount):
        if amount < 0:
            logger.warning(f"Trying to add negative amount: {amount}")
            print("You try to add negative amount of money!")
            return

        remaining = amount

        # Sorting money to chips
        for denomination in [100, 25, 5, 1]:
            if remaining >= denomination:
                count = remaining // denomination
                self.chips[denomination].quantity += count
                remaining %= denomination

    def total_value(self) -> int:
        '''Total value of chips'''
        total = 0
        for chip in self.chips.values():
            total += chip.chip_total_value()
        return total

    def add(self, amount: int):
        """Add money to chips with a conversion"""
        self._add_money(amount)
        logger.info(f"Added {amount} to chips")

    def remove(self, amount: int) -> bool:
        """Remove chips from balance if it possible"""
        if self.total_value() < amount:
            logger.warning(
                f"Unable to remove {amount}, there is only {self.total_value()} chips")
            print(
                f"Unable to remove {amount} chips from your balance. You have only {self.total_value()}")
            return False

        # Subtract from current sum and recalculate values
        current_total = self.total_value()
        new_total = current_total - amount

        # Remove all chips
        for chip in self.chips.values():
            chip.quantity = 0

        # Add new sum
        self._add_money(new_total)

        logger.info(f"Removed {amount} chips from balance")
        return True

    def get_info(self) -> str:
        """Current state of chips"""
        info = []
        for denomination in [100, 25, 5, 1]:
            chips_quantity = self.chips[denomination].quantity
            if chips_quantity > 0:
                info.append(f"{denomination}:{chips_quantity}")
        return ", ".join(info) if info else "no chips"

    def __repr__(self) -> str:
        return f"Chips: {self.get_info()}"
