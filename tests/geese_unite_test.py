from src.events.geese_unite import GeeseUniteEvent
from unittest.mock import Mock, patch


class TestGeeseUniteEventSimple:

    def test_unite_two_geese_success(self):
        # Prepare
        mock_casino = Mock()
        goose1 = Mock()
        goose1.name = "First"
        goose2 = Mock()
        goose2.name = "Second"
        mock_casino.geese = [goose1, goose2]

        event = GeeseUniteEvent(mock_casino)

        with patch('random.choice', side_effect=[goose1, goose2]):
            goose1.__add__ = Mock(return_value=Mock())

            # Action
            result = event.geese_unite_event()

            # Check
            assert result is True
            assert mock_casino.geese.remove.call_count == 2
            assert mock_casino.geese.append.call_count == 1

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

    def test_unite_with_golden_goose_collects_money(self):
        # Prepare
        mock_casino = Mock()
        goose1 = Mock()
        goose1.name = "RegularGoose"
        golden_goose = Mock()
        golden_goose.name = "GoldenGoose"
        golden_goose.collect_from_geese = Mock(return_value=100)
        mock_casino.geese = [goose1, golden_goose]
        event = GeeseUniteEvent(mock_casino)
        with patch('random.choice', side_effect=[goose1, golden_goose]):
            group_mock = Mock()
            group_mock.name = "Group of 2 geese"
            group_mock.geese = [goose1, golden_goose]
            goose1.__add__ = Mock(return_value=group_mock)
            with patch('builtins.print') as mock_print:

                # Action
                result = event.geese_unite_event()

                # Check
                assert result is True
                golden_goose.collect_from_geese.assert_called_once_with(
                    mock_casino.geese)
                mock_print.assert_any_call(
                    f"[🦢🦢💰 Unite]: {goose1.name}+{golden_goose.name} formed {group_mock.name}! Golden goose collected 100!"
                )
