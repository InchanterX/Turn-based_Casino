from unittest.mock import Mock, patch
from src.infrastructure.goose import GoldenGoose, Goose
from src.events.goose_attack import GooseAttackEvent


class TestGooseAttackEvent:
    def test_attack_logic(self):
        mock_casino = Mock()
        event = GooseAttackEvent(mock_casino)

        event.instruments = Mock()

        event.instruments.random_player.return_value = None
        assert event.goose_attack_event() is False

        player = Mock(name="Player1")
        golden = Mock(spec=GoldenGoose)
        golden.name = "Goldie"
        golden.attack_player.return_value = 100

        event.instruments.random_player.return_value = player
        event.instruments.random_goose.return_value = golden

        assert event.goose_attack_event() is True

        normal_goose = Mock(spec=Goose)
        normal_goose.name = "Normal"
        event.instruments.random_goose.return_value = normal_goose

        with patch('builtins.input', return_value=''):
            assert event.goose_attack_event() is True
