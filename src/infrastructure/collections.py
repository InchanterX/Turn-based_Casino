class Player_Collection:
    def __init__(self):
        self._players = []

    def __getitem__(self, index):
        return self._players[index]

    def __len__(self):
        return len(self._players)

    def __iter__(self):
        return iter(self._players)

    def append(self, player):
        self._players.append(player)

    def remove(self, player):
        self._players.remove(player)


class Goose_Collection:
    def __init__(self):
        self._geese = []

    def __getitem__(self, index):
        return self._geese[index]

    def __len__(self):
        return len(self._geese)

    def __iter__(self):
        return iter(self._geese)

    def append(self, goose):
        self._geese.append(goose)

    def remove(self, goose):
        self._geese.remove(goose)


class Casino_Collection:
    def __init__(self):
        self._casino_balance = {}
