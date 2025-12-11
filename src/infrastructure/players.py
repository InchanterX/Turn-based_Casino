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
