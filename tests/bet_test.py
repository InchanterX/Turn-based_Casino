from src.infrastructure.constants import SYMBOLS, MULTIPLIERS
from unittest.mock import Mock, patch
from src.events.bet import BetEvent
from src.infrastructure.casino import Casino


class TestBetEvent:

    def test_init(self):
        # Prepare
        mock_casino = Mock()

        # Action
        event = BetEvent(mock_casino)

        # Check
        assert event.casino == mock_casino
        assert event.instruments is not None
        assert event.instruments.casino == mock_casino

    def test_get_player_returns_none_when_no_players(self):
        # Prepare
        mock_casino = Mock()
        mock_instruments = Mock()
        mock_instruments.random_player.return_value = None
        event = BetEvent(mock_casino)
        event.instruments = mock_instruments

        # Action
        result = event._get_player()

        # Check
        assert result is None
        mock_instruments.random_player.assert_called_once()

    def test_get_player_returns_player(self):
        # Prepare
        mock_casino = Mock()
        mock_player = Mock()
        mock_instruments = Mock()
        mock_instruments.random_player.return_value = mock_player
        event = BetEvent(mock_casino)
        event.instruments = mock_instruments

        # Action
        result = event._get_player()

        # Check
        assert result == mock_player

    def test_convert_to_int_valid(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)

        # Action
        result = event._convert_to_int("100")

        # Check
        assert result == 100

    def test_convert_to_int_invalid(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)

        with patch('builtins.print') as mock_print:
            with patch('src.infrastructure.logger.logger.exception') as mock_logger:
                # Action
                result = event._convert_to_int("abc")

                # Check
                assert result is None
                mock_logger.assert_called_once()
                mock_print.assert_called_once_with(
                    "[⚙️] Invalid input data! Enter a number!")

    def test_sell_from_inventory(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)
        mock_player = Mock()
        mock_player.balance = 500

        with patch('builtins.print') as mock_print:
            # Action
            event._sell_from_inventory(mock_player)

            # Check
            mock_print.assert_called_once_with(
                "You should sell something from your inventory. You have: 500\n")

    def test_ask_until_valid_valid_input(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)
        mock_player = Mock()
        mock_player.name = "TestPlayer"
        mock_player.balance = 1000
        mock_player.get_chips_value.return_value = 500

        test_inputs = ["200"]

        with patch('builtins.input', side_effect=test_inputs):
            with patch.object(event, '_convert_to_int', return_value=200):
                # Action
                result = event._ask_until_valid(mock_player, "Test message")

                # Check
                assert result == 200

    def test_ask_until_valid_negative_then_valid(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)
        mock_player = Mock()
        mock_player.name = "TestPlayer"
        mock_player.balance = 1000
        mock_player.get_chips_value.return_value = 500

        test_inputs = ["-100", "200"]

        with patch('builtins.input', side_effect=test_inputs):
            with patch.object(event, '_convert_to_int', side_effect=[-100, 200]):
                with patch('builtins.print') as mock_print:
                    with patch('src.infrastructure.logger.logger.warning') as mock_logger:
                        # Action
                        result = event._ask_until_valid(
                            mock_player, "Test message")

                        # Check
                        assert result == 200
                        mock_logger.assert_called_once_with(
                            "Player TestPlayer tried to enter a negative quantity.")
                        mock_print.assert_called_once_with(
                            "[⚙️] This is illegal! Enter a positive integer!")

    def test_ask_until_valid_overflow_then_valid(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)
        mock_player = Mock()
        mock_player.name = "TestPlayer"
        mock_player.balance = 1000
        mock_player.get_chips_value.return_value = 500

        test_inputs = ["2000", "800"]

        with patch('builtins.input', side_effect=test_inputs):
            with patch.object(event, '_convert_to_int', side_effect=[2000, 800]):
                with patch('builtins.print') as mock_print:
                    with patch('src.infrastructure.logger.logger.warning') as mock_logger:
                        # Action
                        result = event._ask_until_valid(
                            mock_player, "Test message")

                        # Check
                        assert result == 800
                        mock_logger.assert_called_once_with(
                            "Player TestPlayer tried to enter an overflowing quantity.")
                        mock_print.assert_called_once_with(
                            "[⚙️] This is illegal! You have only 1000 money and 500 chips on your balance (1500 in total)!")

    def test_convert_money(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)
        mock_player = Mock()
        mock_player.name = "TestPlayer"
        mock_player.balance = 1000

        with patch.object(event, '_ask_until_valid', return_value=300):
            with patch('src.infrastructure.logger.logger.info') as mock_logger:
                # Action
                event._convert_money(mock_player)

                # Check
                mock_player.balance_lesion.assert_called_once_with(300)
                mock_player.chips_income.assert_called_once_with(300)
                mock_logger.assert_called_once_with(
                    "Successfully converted TestPlayer's 300 money to chips.")

    def test_get_symbol_weights_base_case(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)

        # Action
        weights = event._get_symbol_weights(0)

        # Check
        assert len(weights) == 5
        assert all(w > 0 for w in weights)

    def test_get_symbol_weights_with_luck(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)

        # Action
        weights_luck_0 = event._get_symbol_weights(0)
        weights_luck_50 = event._get_symbol_weights(50)

        # Check
        assert len(weights_luck_0) == len(weights_luck_50) == 5
        assert weights_luck_0 != weights_luck_50

    def test_calculate_payout_three_of_a_kind(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)

        bet_amount = 100

        for symbol in SYMBOLS:
            # Action
            payout = event._calculate_payout(
                [symbol, symbol, symbol], bet_amount)

            # Check
            expected = int(bet_amount * MULTIPLIERS[symbol] * 3)
            assert payout == expected

    def test_calculate_payout_two_of_a_kind(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)

        bet_amount = 100

        test_cases = [
            (['🍎', '🍎', '🍌'], '🍎'),
            (['🍌', '🍎', '🍎'], '🍎'),
            (['🍌', '🍌', '🍎'], '🍌'),
        ]

        for slots, expected_symbol in test_cases:
            # Action
            payout = event._calculate_payout(slots, bet_amount)

            # Check
            expected = int(bet_amount * MULTIPLIERS[expected_symbol] * 1.5)
            assert payout == expected

    def test_calculate_payout_first_and_third_same(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)

        bet_amount = 100
        slots = ['🍎', '🍌', '🍎']

        # Action
        payout = event._calculate_payout(slots, bet_amount)

        # Check
        expected = int(bet_amount * MULTIPLIERS['🍎'] * 1.5)
        assert payout == expected

    def test_calculate_payout_valuable_symbols(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)

        bet_amount = 100

        valuable_cases = [
            ['🍍', '🍎', '🍌'],
            ['🍎', '🍒', '🍌'],
            ['🍌', '🍎', '🍍'],
        ]

        for slots in valuable_cases:
            # Action
            payout = event._calculate_payout(slots, bet_amount)

            # Check
            expected = int(bet_amount * 0.1)
            assert payout == expected

    def test_calculate_payout_no_win(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)

        bet_amount = 100
        slots = ['🍎', '🍌', '🍊']

        # Action
        payout = event._calculate_payout(slots, bet_amount)

        # Check
        assert payout == 0

    def test_player_bet_event_no_players(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)

        with patch.object(event, '_get_player', return_value=None):
            with patch('builtins.print') as mock_print:
                with patch('src.infrastructure.logger.logger.warning') as mock_logger:
                    # Action
                    result = event.player_bet_event()

                    # Check
                    assert result is False
                    mock_logger.assert_called_once_with(
                        "No players to place bets.")
                    mock_print.assert_called_once_with(
                        "No players to place bets!")

    def test_player_bet_event_not_enough_total(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)
        mock_player = Mock()
        mock_player.name = "TestPlayer"
        mock_player.balance = 100
        mock_player.get_chips_value.return_value = 50

        with patch.object(event, '_get_player', return_value=mock_player):
            with patch.object(event, '_ask_until_valid', return_value=200):
                with patch('builtins.print') as mock_print:
                    with patch.object(event, '_sell_from_inventory') as mock_sell:
                        # Action
                        result = event.player_bet_event()

                        # Check
                        assert result is True
                        mock_print.assert_called_once_with(
                            "[🎰] TestPlayer wanted to bet but only 150 available!")
                        mock_sell.assert_called_once_with(mock_player)

    def test_player_bet_event_not_enough_chips(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)
        mock_player = Mock()
        mock_player.name = "TestPlayer"
        mock_player.balance = 1000

        mock_player.get_chips_value.side_effect = [
            50, 50, 250, 250]

        with patch.object(event, '_get_player', return_value=mock_player):
            with patch.object(event, '_ask_until_valid', return_value=200):
                with patch('builtins.print') as mock_print:
                    with patch.object(event, '_convert_money') as mock_convert:
                        # Action
                        result = event.player_bet_event()

                        # Check
                        assert result is True
                        mock_convert.assert_called_once_with(mock_player)
                        assert mock_print.call_count >= 1

    def test_player_bet_event_successful_bet(self):
        # Prepare
        mock_casino = Mock()
        event = BetEvent(mock_casino)
        mock_player = Mock()
        mock_player.name = "TestPlayer"
        mock_player.balance = 1000
        mock_player.get_chips_value.return_value = 500

        with patch.object(event, '_get_player', return_value=mock_player):
            with patch.object(event, '_ask_until_valid', return_value=200):
                with patch.object(event, '_fancy_spin', return_value=['🍎', '🍎', '🍎']):
                    with patch('time.sleep'):
                        with patch('builtins.print'):
                            with patch.object(event, '_calculate_payout', return_value=150):
                                # Action
                                result = event.player_bet_event()

                                # Check
                                assert result is True
                                mock_player.chips_lesion.assert_called_once_with(
                                    200)
                                mock_player.chips_income.assert_called_once_with(
                                    150)

    def test_player_bet_event_with_real_player(self):
        # Prepare
        casino = Casino()
        casino.register_default("TestPlayer")
        event = BetEvent(casino)

        player = casino.players[0]
        player.balance = 1000
        player.chips.add(500)

        with patch('builtins.input', return_value="100"):
            with patch.object(event, '_fancy_spin', return_value=['🍎', '🍎', '🍎']):
                with patch('time.sleep'):
                    with patch('builtins.print'):
                        # Action
                        result = event.player_bet_event()

                        # Check
                        assert result is True
