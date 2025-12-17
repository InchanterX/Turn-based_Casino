import time
from src.infrastructure.constants import SYMBOLS, MULTIPLIERS
from random import choice
from src.infrastructure.logger import logger
from src.infrastructure.events_instruments import EventsInstruments


class BetEvent:
    def __init__(self, casino):
        self.casino = casino
        self.instruments = EventsInstruments(casino)

    def _get_player(self):
        '''Literally get random player'''
        return self.instruments.random_player()

    def _convert_to_int(self, input_str: str) -> int | None:
        '''
        Convert input string into integer type if it is possible.
        Otherwise return None
        '''
        try:
            return int(input_str)
        except ValueError:
            logger.exception(
                f"Invalid input data. Unable convert {input_str} to int.")
            print("[⚙️] Invalid input data! Enter a number!")
            return None

    def _sell_from_inventory(self, player):
        '''Ask player to sell something from the inventory'''
        print(
            f"You should sell something from your inventory. You have: {player.balance}\n")

    def _ask_until_valid(self, player, message: str) -> int:
        '''Ask player to input positive integer number that is not greater then current total balance'''
        while True:
            raw_input = input(message)
            bet_amount = self._convert_to_int(raw_input)
            if bet_amount is None:
                continue
            if bet_amount < 0:
                logger.warning(
                    f"Player {player.name} tried to enter a negative quantity.")
                print("[⚙️] This is illegal! Enter a positive integer!")
                continue
            if bet_amount > (player.balance + player.get_chips_value()):
                logger.warning(
                    f"Player {player.name} tried to enter an overflowing quantity.")
                print(
                    f"[⚙️] This is illegal! You have only {player.balance} money and {player.get_chips_value()} chips on your balance ({player.get_chips_value() + player.balance} in total)!")
                continue
            break
        return bet_amount

    def _convert_money(self, player):
        '''Convert input amount of money and transfer them to the chips with conversion'''
        amount = self._ask_until_valid(
            player, f"[🎰] How much money do you want to convert to chips? (available: {player.balance})\n > ")
        player.balance_lesion(amount)
        player.chips_income(amount)
        logger.info(
            f"Successfully converted {player.name}'s {amount} money to chips.")

    @staticmethod
    def _fancy_spin(duration: int = 3):
        print("\n🎰 Spin...")

        # Start fast and slowly slow it
        delays = [0.05] * 10 + [0.1] * 5 + [0.2] * 3 + [0.3, 0.5, 0.7]

        # Spin animation
        for delay in delays:
            temp_slots = [choice(SYMBOLS) for _ in range(3)]
            print(f"\r🎰|{'|'.join(temp_slots)}|", end="", flush=True)
            time.sleep(delay)

        # Final result
        final_slots = [choice(SYMBOLS) for _ in range(3)]
        print(f"\r🎰|{'|'.join(final_slots)}|")

        return final_slots

    def _calculate_payout(self, slots):
        # Count payout
        if slots[0] == slots[1] == slots[2]:
            symbol = slots[0]
            return MULTIPLIERS[symbol]*100
        elif slots[0] == slots[1] or slots[1] == slots[2]:
            symbol = slots[1]
            return MULTIPLIERS[symbol]*20
        elif slots[0] == slots[2]:
            symbol = slots[0]
            return MULTIPLIERS[symbol]*20
        else:
            return 0

    def player_bet_event(self) -> bool:
        '''Event of player making a bet'''
        player = self._get_player()
        if player is None:
            logger.warning("No players to place bets.")
            print("No players to place bets!")
            return False

        bet_amount = self._ask_until_valid(
            player, f"[🎰] Gamble time! Enter bet amount (available chips: {player.get_chips_value()}, money: {player.balance}):\n > ")

        if (player.get_chips_value() + player.balance) < bet_amount:
            print(
                f"[🎰] {player.name} wanted to bet but only {player.balance + player.get_chips_value()} available!")
            self._sell_from_inventory(player)
            return True
        while player.get_chips_value() < bet_amount:
            print(
                f"[🎰] {player.name} wanted to bet but there is not enough chips. Try to convert them from your balance.")
            self._convert_money(player)

        slots = self._fancy_spin()
        # slots = [random.choice(SYMBOLS) for _ in range(3)]
        # print(f"🎰|{'|'.join(slots)}|")
        player.chips_lesion(bet_amount)
        payout = self._calculate_payout(slots)
        print(payout)
        player.chips_lesion(payout)
        return True

        # # 45/55 chance
        # if random() < 0.45:
        #     # Win from 1.5 to 3.0 times
        #     multiplier = random() * 1.5 + 1.5
        #     win_amount = int(bet_amount * multiplier)
        #     player.chips_income(win_amount)
        #     logger.info(
        #         f"Player {player.name} won {win_amount} from bet {bet_amount}")
        #     print(
        #         f"[🎰 Bet Win]: {player.name} bet {bet_amount} and won {win_amount}!")
        #     return True
        # else:
        #     # Lose
        #     player.chips_lesion(bet_amount)
        #     logger.info(f"Player {player.name} lost {bet_amount} in bet")
        #     print(f"[🎰 Bet Loss]: {player.name} lost {bet_amount} in a bet!")
        #     return True
