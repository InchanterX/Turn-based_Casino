from time import sleep
from src.infrastructure.constants import SYMBOLS, MULTIPLIERS
from random import choices
from src.infrastructure.logger import logger
from src.infrastructure.events_instruments import EventsInstruments


class BetEvent:
    '''Ask player to make a bet, display the spin animation of roulette, count the result based on luck level, change user balance'''

    def __init__(self, casino):
        self.casino = casino
        self.instruments = EventsInstruments(casino)

    def _get_player(self):
        '''Literally get random player'''
        logger.debug("Selecting random player for betting event.")
        return self.instruments.random_player()

    def _convert_to_int(self, input_str: str) -> int | None:
        '''
        Convert input string into integer type if it is possible.
        Otherwise return None
        '''
        try:
            logger.debug(f"Converting input {input_str} to int.")
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

    def _fancy_spin(self, player):
        print("\n🎰 Spin...")

        weights = self._get_symbol_weights(player.luck)

        # Start fast and slowly slow it
        delays = [0.05] * 10 + [0.1] * 5 + [0.2] * 3 + [0.3, 0.5, 0.7]

        # Spin animation
        for delay in delays:
            temp_slots = choices(SYMBOLS, weights=weights, k=3)
            print(f"\r🎰|{'|'.join(temp_slots)}|", end="", flush=True)
            sleep(delay)

        # Final result
        final_slots = choices(SYMBOLS, weights=weights, k=3)
        print(f"\r🎰|{'|'.join(final_slots)}|")
        logger.info(
            f"Player {player.name} spun the slots: {'|'.join(final_slots)}")
        return final_slots

    def _get_symbol_weights(self, luck: int):
        """
        Return recalculated weight of symbols according to player's luck
        """
        # Base case (luck: 0)
        base_weights = {
            '🍎': 30,   # 40%
            '🍊': 30,   # 30%
            '🍌': 20,   # 15%
            '🍍': 15,   # 10%
            '🍒': 5      # 5%
        }

        # Luck coefficient per unit
        luck_multiplier = 0.3

        weights = []
        for symbol in SYMBOLS:
            base_weight = base_weights[symbol]

            # increase weight of good symbols, decrease chance of bad
            if symbol == '🍎':
                adjusted = base_weight * (1 - luck * luck_multiplier / 100)
            elif symbol == '🍊':
                adjusted = base_weight * (1 - luck * luck_multiplier / 200)
            elif symbol == '🍌':
                adjusted = base_weight
            elif symbol == '🍍':
                adjusted = base_weight * (1 + luck * luck_multiplier / 100)
            else:
                adjusted = base_weight * (1 + luck * luck_multiplier / 50)

            weights.append(max(1, int(adjusted)))

        return weights

    def _calculate_payout(self, slots, bet_amount: int) -> int:
        '''Calculate payout based on slots and bet amount'''
        # Count payout
        if slots[0] == slots[1] == slots[2]:
            symbol = slots[0]
            return int(bet_amount * MULTIPLIERS[symbol] * 3)  # x3 for 3
        elif slots[0] == slots[1] or slots[1] == slots[2]:
            symbol = slots[1]
            return int(bet_amount * MULTIPLIERS[symbol] * 1.5)  # x1.5 for 2
        elif slots[0] == slots[2]:
            symbol = slots[0]
            return int(bet_amount * MULTIPLIERS[symbol] * 1.5)  # x1.5 for 2
        else:
            # Grants for valuable symbols
            valuable_symbols = ['🍍', '🍒']
            for symbol in valuable_symbols:
                if symbol in slots:
                    return int(bet_amount * 0.1)  # return 10% of bet
            return 0

    def player_bet_event(self) -> bool:
        '''Event of player making a bet'''
        # print("BET")
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
            logger.info(
                f"Player {player.name} has insufficient chips for the bet. Initiating conversion from balance.")
            print(
                f"[🎰] {player.name} wanted to bet but there is not enough chips. Try to convert them from your balance.")
            self._convert_money(player)

        slots = self._fancy_spin(player)
        sleep(0.5)
        player.chips_lesion(bet_amount)
        payout = self._calculate_payout(slots, bet_amount)
        print(payout)
        player.chips_income(payout)
        logger.info(
            f"Player {player.name} bet {bet_amount} and won {payout} from the slots.")
        return True
