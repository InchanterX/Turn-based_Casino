from unittest.mock import Mock
from src.events.goose_steal import GooseStealEvent


class TestGooseStealEvent:

    def test_coverage_no_entities(self):
        mock_casino = Mock()
        event = GooseStealEvent(mock_casino)
        event.instruments = Mock()

        event.instruments.random_player.return_value = None
        event.instruments.random_goose.return_value = Mock()

        assert event.goose_steal_event() is True

    def test_coverage_successful_steal(self):
        mock_casino = Mock()
        event = GooseStealEvent(mock_casino)
        event.instruments = Mock()

        player = Mock(name="RichPlayer")
        goose = Mock()
        goose.name = "ThiefGoose"
        goose.steal_from_player.return_value = 50

        event.instruments.random_player.return_value = player
        event.instruments.random_goose.return_value = goose

        assert event.goose_steal_event() is True
        goose.steal_from_player.assert_called_once_with(player)

    def test_coverage_failed_steal(self):
        mock_casino = Mock()
        event = GooseStealEvent(mock_casino)
        event.instruments = Mock()

        player = Mock()
        goose = Mock()
        goose.name = "ClumsyGoose"
        goose.steal_from_player.return_value = 0

        event.instruments.random_player.return_value = player
        event.instruments.random_goose.return_value = goose

        assert event.goose_steal_event() is True

    def test_coverage_goose_cannot_steal(self):
        mock_casino = Mock()
        event = GooseStealEvent(mock_casino)
        event.instruments = Mock()

        player = Mock()
        goose = Mock()
        goose.name = "PeacefulGoose"
        del goose.steal_from_player

        event.instruments.random_player.return_value = player
        event.instruments.random_goose.return_value = goose

        assert event.goose_steal_event() is True
