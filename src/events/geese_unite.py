from src.infrastructure.logger import logger
from random import choice


class GeeseUniteEvent:
    '''Unite geese into groups using magical method'''

    def __init__(self, casino):
        self.casino = casino

    def geese_unite_event(self) -> str:
        '''Two geese unite into a group'''
        if len(self.casino.geese) < 2:
            return "[🦢 Geese] Not enough geese to unite"

        goose1 = choice(self.casino.geese)
        other_geese = [
            goose for goose in self.casino.geese if goose != goose1]
        if not other_geese:
            return "[🦢 Geese] No other geese to unite with"

        goose2 = choice(other_geese)

        # Use magical __add__
        group = goose1 + goose2

        # Rearrange goose
        self.casino.geese.remove(goose1)
        self.casino.geese.remove(goose2)
        self.casino.geese.append(group)

        logger.info(
            f"Geese {goose1.name} and {goose2.name} united into group")

        # In case of GoldenGoose party
        if hasattr(group, 'geese'):
            for goose in group.geese:
                if hasattr(goose, 'collect_from_geese'):
                    collected = goose.collect_from_geese(self.casino.geese)
                    if collected > 0:
                        return f"[🦢🦢💰 Unite]: {goose1.name}+{goose2.name} formed {group.name}! Golden goose collected {collected}!"

        return f"[🦢🦢 Unite]: {goose1.name} and {goose2.name} united into {group.name}!"
