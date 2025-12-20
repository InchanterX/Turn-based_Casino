from src.infrastructure.logger import logger


class PlayerCollection:
    def __init__(self, players=None):
        self._players = players if players is not None else []

    def __getitem__(self, index):
        if isinstance(index, slice):
            return type(self)(self._players[index])
        return self._players[index]

    def __len__(self):
        return len(self._players)

    def __iter__(self):
        return iter(self._players)

    def append(self, player):
        logger.info(f"Adding player {player.name} to collection.")
        self._players.append(player)

    def remove(self, player):
        logger.info(f"Removing player {player.name} from collection.")
        self._players.remove(player)
