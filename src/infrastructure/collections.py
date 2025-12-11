class Player_Collection:
    def __init__(self):
        self._players = []

    def __getitem__(self, index):
        return self._players[index]

    def __len__(self):
        return len(self._players)

    def addend(self, player):
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

    def addend(self, goose):
        self._geese.append(goose)

    def remove(self, goose):
        self._geese.remove(goose)
