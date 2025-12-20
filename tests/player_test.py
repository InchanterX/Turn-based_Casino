from unittest.mock import patch
from src.infrastructure.player import Player


class TestPlayerSimple:

    def test_player_initial_state(self):
        # Prepare and Action
        player = Player("Alice", 200)

        # Check
        assert player.name == "Alice"
        assert player.balance == 200
        assert player.health > 0
        assert player.luck > 0
        assert callable(player.is_alive)

    def test_health_operations(self):
        # Prepare and Action
        player = Player("Test", 100)
        start_health = player.health

        player.lose_health(10)
        assert player.health == start_health - 10

        player.increase_health(5)
        assert player.health == start_health - 5

    def test_luck_operations(self):
        player = Player("Test", 100)
        start_luck = player.luck

        player.decrease_luck(3)
        assert player.luck == start_luck - 3

        player.increase_luck(2)
        assert player.luck == start_luck - 1

    def test_balance_operations(self):
        player = Player("Test", 100)

        player.balance_income(50)
        assert player.balance == 150

        player.balance_lesion(70)
        assert player.balance == 80

    def test_is_alive_edge_cases(self):
        player = Player("Test", 100)

        player.health = 1
        assert player.is_alive() is True

        player.health = 0
        assert player.is_alive() is False

        player.health = -1
        assert player.is_alive() is False


def test_roll_the_dice_returns_patched_value_and_prints():
    # Prepare
    player = Player("Dice", 50)

    # Action
    with patch('src.infrastructure.player.randint', return_value=4):
        with patch('builtins.print') as mock_print:
            result = player.roll_the_dice()

    # Check
    assert result == 4
    mock_print.assert_called_with("[🎲] You rolled 4!")


def test_repr_reflects_status_health_luck_and_chips():
    # Prepare
    player = Player("Bob", 100)
    player.health = 10
    player.luck = 5

    # Action
    with patch.object(Player, 'get_chips_value', return_value=250):
        s = player._repr__()

    # Check
    assert "Player Bob is alive" in s
    assert "has 10HP" in s
    assert "5 units of luck" in s
    assert "chips: 250" in s


def test_repr_shows_dead_status_when_health_zero():
    # Prepare
    player = Player("Eve", 100)
    player.health = 0
    player.luck = 0

    # Action
    with patch.object(Player, 'get_chips_value', return_value=0):
        s = player._repr__()

    # Check
    assert "is dead" in s
    assert "has 0HP" in s
    assert "0 units of luck" in s
    assert "chips: 0" in s
