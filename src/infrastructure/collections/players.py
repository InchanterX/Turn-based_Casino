from src.infrastructure.logger import logger


class PlayerCollection:
    def __init__(self, players=None):
        self._players = players if players is not None else []

    def __getitem__(self, index):
        '''Get a player or a slice of players from the collection'''
        if isinstance(index, slice):
            return type(self)(self._players[index])
        return self._players[index]

    def __len__(self):
        '''Return the number of players in the collection'''
        return len(self._players)

    def __iter__(self):
        '''Return an iterator over the players in the collection'''
        return iter(self._players)

    def append(self, player):
        '''Add a player to the collection'''
        logger.info(f"Adding player {player.name} to collection.")
        self._players.append(player)

    def remove(self, player):
        '''Remove a player from the collection'''
        logger.info(f"Removing player {player.name} from collection.")
        self._players.remove(player)
