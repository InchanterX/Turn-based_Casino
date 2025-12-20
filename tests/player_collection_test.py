import pytest
from src.infrastructure.collections.players import PlayerCollection
from unittest.mock import Mock


class TestPlayerCollection:

    def test_init(self):
        # Action
        collection = PlayerCollection()

        # Check
        assert len(collection) == 0
        assert collection._players == []

    def test_append(self):
        # Prepare
        collection = PlayerCollection()
        mock_player = Mock()

        # Action
        collection.append(mock_player)

        # Check
        assert len(collection) == 1
        assert collection._players[0] == mock_player

    def test_append_multiple(self):
        # Prepare
        collection = PlayerCollection()
        mock_players = [Mock(), Mock(), Mock()]

        # Action
        for player in mock_players:
            collection.append(player)

        # Check
        assert len(collection) == 3
        assert collection._players == mock_players

    def test_len(self):
        # Prepare
        collection = PlayerCollection()
        collection._players = [Mock(), Mock()]

        # Action and Check
        assert len(collection) == 2
        assert collection.__len__() == 2

    def test_getitem_int(self):
        # Prepare
        collection = PlayerCollection()
        mock_player1 = Mock()
        mock_player2 = Mock()
        collection._players = [mock_player1, mock_player2]

        # Action and Check
        assert collection[0] == mock_player1
        assert collection[1] == mock_player2

    def test_getitem_slice(self):
        # Prepare
        collection = PlayerCollection()
        mock_players = [Mock(), Mock(), Mock(), Mock()]
        collection._players = mock_players

        # Action
        result = collection[1:3]

        # Check
        assert isinstance(result, PlayerCollection)
        assert len(result) == 2
        assert result._players == mock_players[1:3]

    def test_getitem_slice_empty(self):
        # Prepare
        collection = PlayerCollection()
        mock_players = [Mock(), Mock()]
        collection._players = mock_players

        # Action
        result = collection[10:20]

        # Check
        assert isinstance(result, PlayerCollection)
        assert len(result) == 0
        assert result._players == []

    def test_getitem_negative_index(self):
        # Prepare
        collection = PlayerCollection()
        mock_player1 = Mock()
        mock_player2 = Mock()
        collection._players = [mock_player1, mock_player2]

        # Action and Check
        assert collection[-1] == mock_player2
        assert collection[-2] == mock_player1

    def test_remove(self):
        # Prepare
        collection = PlayerCollection()
        mock_player1 = Mock()
        mock_player2 = Mock()
        collection._players = [mock_player1, mock_player2]

        # Action
        collection.remove(mock_player1)

        # Check
        assert len(collection) == 1
        assert collection._players == [mock_player2]

    def test_remove_last(self):
        # Prepare
        collection = PlayerCollection()
        mock_player = Mock()
        collection._players = [mock_player]

        # Action
        collection.remove(mock_player)

        # Check
        assert len(collection) == 0
        assert collection._players == []

    def test_iter(self):
        # Prepare
        collection = PlayerCollection()
        mock_players = [Mock(), Mock(), Mock()]
        collection._players = mock_players

        # Action
        result = list(collection)

        # Check
        assert result == mock_players
        for i, player in enumerate(collection):
            assert player == mock_players[i]

    def test_multiple_operations(self):
        collection = PlayerCollection()
        player1 = Mock()
        player2 = Mock()
        player3 = Mock()

        # Добавляем
        collection.append(player1)
        collection.append(player2)

        assert len(collection) == 2
        assert collection[0] == player1

        collection.append(player3)
        assert len(collection) == 3

        collection.remove(player2)
        assert len(collection) == 2
        assert collection._players == [player1, player3]

        players = []
        for player in collection:
            players.append(player)
        assert players == [player1, player3]

    def test_empty_collection(self):
        collection = PlayerCollection()

        assert len(collection) == 0
        assert list(collection) == []

        with pytest.raises(IndexError):
            _ = collection[0]

        result = collection[:]
        assert isinstance(result, PlayerCollection)
        assert len(result) == 0
