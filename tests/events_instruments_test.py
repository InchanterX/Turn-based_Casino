from src.infrastructure.events_instruments import EventsInstruments
from src.infrastructure.player import Player
from src.infrastructure.casino import Casino
from src.infrastructure.goose import Goose


class TestEventsInstrumentsSimple:

    def test_always_returns_something_when_available(self):
        # Prepare
        casino = Casino()
        player = Player("Test", 100)
        goose = Goose("Gus")
        casino.players.append(player)
        casino.geese.append(goose)

        # Action
        instruments = EventsInstruments(casino)

        # Check
        assert instruments.random_player() == player
        assert instruments.random_goose() == goose

    def test_returns_none_when_empty(self):
        # Prepare
        casino = Casino()

        # Action
        instruments = EventsInstruments(casino)

        # Check
        assert instruments.random_player() is None
        assert instruments.random_goose() is None

    def test_works_with_real_casino_setup(self):
        # Prepare
        casino = Casino()
        casino.register_default("Alex")

        # Action
        instruments = EventsInstruments(casino)

        # Prepare
        player = instruments.random_player()
        assert player is not None
        assert player.name == "Alex"

        goose = instruments.random_goose()
        assert goose is not None
        assert goose in casino.geese
