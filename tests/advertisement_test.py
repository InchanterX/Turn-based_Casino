from unittest.mock import Mock, patch
from src.events.advertisement import AdvertisementEvent


class TestAdvertisementEvent:

    def test_init(self):
        # Prepare
        mock_casino = Mock()

        # Action
        event = AdvertisementEvent(mock_casino)

        # Check
        assert event.casino == mock_casino

    def test_advertisement_event_returns_true(self):
        # Prepare
        mock_casino = Mock()
        event = AdvertisementEvent(mock_casino)

        with patch('random.choice') as mock_choice:
            mock_choice.return_value = "Test Adv"

            # Action
            result = event.advertisement_event()

            # Check
            assert result is True
