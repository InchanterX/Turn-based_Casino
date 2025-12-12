from src.infrastructure.logger import logger
from src.infrastructure.constants import DEFAULT_PLAYER_HEALTH, DEFAULT_PLAYER_LUCK


class Player:
    def __init__(self, name: str, balance: int):
        self._logger = logger
        self.name = name
        self.balance = balance
        self.luck = DEFAULT_PLAYER_LUCK
        self.health = DEFAULT_PLAYER_HEALTH
        self.chips = {
            "1": 0,
            "5": 0,
            "25": 0,
            "100": 0
        }

    def _list_available_chips(self) -> str:
        '''Return available chips'''
        available_chips = ', '.join(str(key) for key in self.chips.keys())
        return available_chips

    def _is_denomination_valid(self, original_denomination, new_denomination) -> int:
        if original_denomination not in self.chips.keys():
            logger.warning(
                f"Player {self.name} asked for conversion of non-existent denomination {original_denomination}.")
            print(
                f"You don't have chips with denomination of {original_denomination}. Try {self._list_available_chips}.")
            return 1
        elif new_denomination not in self.chips.keys():
            logger.warning(
                f"Player {self.name} asked to convert chips to a non-existent denomination {new_denomination}.")
            print(
                f"You can't convert chips to denomination of {new_denomination}. Try {self._list_available_chips}.")
            return 2
        else:
            return 0

    def income(self, amount: int) -> None:
        '''Increase amount of players chips by the given number.'''
        chips_fluctuation = self.convert_to_chips(amount)
        for denomination in range(4):
            self.chips[str(chips_fluctuation[denomination][0])
                       ] += chips_fluctuation[denomination][1]

    def lesion(self, amount: int) -> None:
        '''Decrease amount of players chips by the given number'''
        chips_fluctuation = self.convert_to_chips(amount)
        for denomination in range(4):
            self.chips[str(chips_fluctuation[denomination][0])
                       ] -= chips_fluctuation[denomination][1]

    def lose_health(self, loss: int) -> None:
        self.health -= loss
        logger.info(f"Player {self.name} lost {loss}HP.")
        print(f"You've lost {loss}HP!")

    def decrease_luck(self, loss: int) -> None:
        self.luck -= loss
        logger.info(
            f"Player {self.name} lost {loss} units of luck. Current state: {self.luck}.")
        print("You've lost some units of luck!")

    def convert_to_chips(self, amount: int) -> list[list[int]]:
        '''Convert given amount of money or chips into optimal amount of chips'''
        output = [
            [1, 0],
            [5, 0],
            [25, 0],
            [100, 0]
        ]
        output[3][1] = amount//100
        amount = amount % 100
        output[2][1] = amount//25
        amount = amount % 25
        output[1][1] = amount//5
        amount = amount % 5
        output[0][1] = amount

        return output

    def recalculate_chips(self, original_denomination: int, desired_quantity: int, new_denomination: int) -> list[bool, str]:
        '''Convert chips from one type to another desirable type'''
        if self._is_denomination_valid(original_denomination, new_denomination):
            logger.warning("Failed to convert chips: invalid denomination.")
            return [False, "Failed to convert chips: invalid denomination."]
        else:
            # not enough chips
            if self.chips[str(original_denomination)] < desired_quantity:
                logger.warning("Failed to convert chips: not enough chips.")
                # print(
                #     f"You have not enough chips (only {self.chips[original_denomination]})")
                return [False, f"You have not enough chips (only {self.chips[str(original_denomination)]})"]

            # uneven quantity
            elif desired_quantity % new_denomination != 0:

                # convert
                self.chips[str(original_denomination)] -= (
                    desired_quantity - (desired_quantity % new_denomination))
                self.chips[str(new_denomination)
                           ] += desired_quantity // new_denomination

                logger.info(
                    f"Partially convert chips from {original_denomination} to {new_denomination}: uneven chips quantity.")
                # print(
                #     f"You gave uneven chips quantity. {desired_quantity // new_denomination} chips of denomination {new_denomination} added to your balance. {desired_quantity // new_denomination} chips left in denomination {original_denomination})")
                return [True, f"You gave uneven chips quantity. {desired_quantity // new_denomination} chips of denomination {new_denomination} added to your balance. {desired_quantity // new_denomination} chips left in denomination {original_denomination})"]

            # even quantity
            else:

                # convert
                self.chips[str(original_denomination)] -= desired_quantity
                self.chips[str(new_denomination)
                           ] += desired_quantity // new_denomination

                logger.info(
                    f"Successfully convert {desired_quantity} chips from {original_denomination} to {new_denomination}.")
                # print(
                #     f"Converted {desired_quantity} chips of denomination {new_denomination}.")
                return [True, f"Converted {desired_quantity} chips of denomination {new_denomination}."]

    def is_alive(self) -> bool:
        if self.health <= 0:
            return False
        return True
