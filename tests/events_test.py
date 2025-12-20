from unittest.mock import Mock, patch
from src.infrastructure.events import Events


class TestEventsSimple:

    def test_get_random_event_always_returns_something(self):
        # Prepare
        mock_casino = Mock()
        events = Events(mock_casino)

        for _ in range(10):
            # Action
            result = events.get_random_event()

            # Check
            assert callable(result)

    def test_events_contain_expected_types(self):
        # Prepare
        mock_casino = Mock()
        events = Events(mock_casino)

        event_names = [name for name, _, _ in events.events]

        assert "bet" in event_names
        assert "goose_attack" in event_names
        assert "goose_steal" in event_names
        assert "geese_unite" in event_names
        assert "advertisement" in event_names
        assert "stroke" in event_names

    def test_event_order_preserved(self):
        # Prepare
        mock_casino = Mock()
        events = Events(mock_casino)

        total = sum(weight for _, weight, _ in events.events)

        for i in range(1, total + 1):
            with patch('random.randint', return_value=i):
                result = events.get_random_event()
                assert callable(result)
