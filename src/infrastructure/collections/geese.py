from src.infrastructure.logger import logger


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
        logger.info(f"Adding goose {goose.name} to collection.")
        self._geese.append(goose)

    def remove(self, goose):
        logger.info(f"Removing goose {goose.name} from collection.")
        self._geese.remove(goose)


# class GeeseIncome:
#     def __init__(self):
#         self._logger = logger
#         self._income = {}

#     def __getitem__(self, goose_name: str):
#         return self._income.get(goose_name, 0)

#     def add_income(self, goose_name, value):
#         current = self._income(goose_name, 0)
#         self._income[goose_name] = current + value
#         logger.info(
#             f"Goose {goose_name} earned {value}. Money in total: {self._income[goose_name]}")
