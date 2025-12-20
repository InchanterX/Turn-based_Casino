from unittest.mock import Mock, patch
from src.events.stroke import StrokeEvent


class TestStrokeEvent:
    @patch('builtins.input', return_value='')
    def test_stroke_logic(self, mock_input):
        mock_casino = Mock()
        event = StrokeEvent(mock_casino)
        event.instruments = Mock()

        player = Mock()
        player.name = "TestPlayer"
        player.roll_the_dice.return_value = 4
        event.instruments.random_player.return_value = player

        result = event.stroke_event()

        assert result is True
        player.lose_health.assert_called_once_with(25)
        player.roll_the_dice.assert_called_once()
