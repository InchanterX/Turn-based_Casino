from src.infrastructure.logger import logger


class PlayerCollection:
    def __init__(self):
        self._players = []

    def __getitem__(self, index: int):
        if isinstance(index, slice):
            return type(self)(self._players[index])
        return self._players[index]

    def __len__(self):
        return len(self._players)

    def __iter__(self):
        return iter(self._players)

    def append(self, player):
        self._players.append(player)

    def remove(self, player):
        self._players.remove(player)
