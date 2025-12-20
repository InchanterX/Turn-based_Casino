from src.infrastructure.logger import logger
from random import choice


class GeeseUniteEvent:
    '''Unite geese into groups using magical method'''

    def __init__(self, casino):
        self.casino = casino

    def geese_unite_event(self) -> bool:
        '''Two geese unite into a group'''
        # print("UNITE")
        if len(self.casino.geese) < 2:
            logger.warning("Not enough geese to unite")
            print("[🦢 Geese]: Not enough geese to unite")
            return False

        goose1 = choice(self.casino.geese)
        other_geese = [
            goose for goose in self.casino.geese if goose != goose1]
        if not other_geese:
            logger.warning("No other geese to unite with")
            print("[🦢 Geese]: No other geese to unite with")
            return False

        goose2 = choice(other_geese)

        # Use magical __add__
        group = goose1 + goose2

        # Rearrange goose
        self.casino.geese.remove(goose1)
        self.casino.geese.remove(goose2)
        self.casino.geese.append(group)

        logger.info(
            f"Geese {goose1.name} and {goose2.name} united into group")
        # print(
        #     f"[🦢🦢 Unite]: {goose1.name} and {goose2.name} united into {group.name}!")

        # In case of GoldenGoose party
        if hasattr(group, 'geese'):
            for goose in group.geese:
                if hasattr(goose, 'collect_from_geese'):
                    collected = goose.collect_from_geese(self.casino.geese)
                    if collected > 0:
                        logger.info(
                            f"Golden goose {goose.name} collected {collected} after uniting.")
                        print(
                            f"[🦢🦢💰 Unite]: {goose1.name}+{goose2.name} formed {group.name}! Golden goose collected {collected}!")
                        return True
        logger.info(
            f"Geese {goose1.name} and {goose2.name} united without golden goose involvement.")
        return True
