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


class GooseCollection:
    def __init__(self):
        self._geese = []

    def __getitem__(self, index):
        if isinstance(index, slice):
            return type(self)(self._geese[index])
        return self._geese[index]

    def __len__(self):
        return len(self._geese)

    def __iter__(self):
        return iter(self._geese)

    def append(self, goose):
        self._geese.append(goose)

    def remove(self, goose):
        self._geese.remove(goose)


class GeeseIncome:
    def __init__(self):
        self._logger = logger
        self._income = {}

    def __getitem__(self, goose_name: str):
        return self._income.get(goose_name, 0)

    def add_income(self, goose_name, value):
        current = self._income(goose_name, 0)
        self._income[goose_name] = current + value
        logger.info(
            f"Goose {goose_name} earned {value}. Money in total: {self._income[goose_name]}")


class CasinoCollection:
    def __init__(self):
        self._logger = logger
        self._balance = 100000
        self._fluctuation = 0

    def gain(self, value):
        self._balance += value
        self._fluctuation += value
        logger.info(
            f"Casino earned {value}. Money in total: {self._balance}. Current fluctuation: {self._fluctuation}")

    def loss(self, value):
        self._balance -= value
        self._fluctuation -= value
        logger.info(
            f"Casino lost {value}. Money in total: {self._balance}. Current fluctuation: {self._fluctuation}")
