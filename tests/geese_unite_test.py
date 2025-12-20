from src.events.geese_unite import GeeseUniteEvent
from unittest.mock import Mock, patch


class TestGeeseUniteEventSimple:

    def test_unite_fails_with_one_goose(self):
        # Prepare
        mock_casino = Mock()
        mock_casino.geese = [Mock()]
        event = GeeseUniteEvent(mock_casino)

        # Action
        result = event.geese_unite_event()

        # Check
        assert result is False

    def test_unite_fails_with_same_goose_twice(self):
        # Prepare
        mock_casino = Mock()
        goose = Mock()
        mock_casino.geese = [goose, goose]
        event = GeeseUniteEvent(mock_casino)

        with patch('random.choice', return_value=goose):
            # Action
            result = event.geese_unite_event()

            # Check
            assert result is False
