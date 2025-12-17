from src.infrastructure.logger import logger


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
