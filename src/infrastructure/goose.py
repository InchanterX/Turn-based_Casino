from src.infrastructure.player import Player


class GooseGroup:
    def __init__(self, geese_list):
        self.geese = geese_list
        self.name = f"Group of {len(geese_list)} geese"

    @property
    def total_health(self):
        return sum(goose.health for goose in self.geese)

    @property
    def total_damage(self):
        return sum(goose.damage for goose in self.geese)

    @property
    def total_balance(self):
        return sum(goose.balance for goose in self.geese)


class Goose:
    '''
    Default Goose class that define goose stats
    '''

    def __init__(self, name: str):
        self.name = name
        self.health = 20
        self.damage = 5
        self.balance = 0

    def __add__(self, other):
        if isinstance(other, Goose):
            return GooseGroup([self, other])
        elif isinstance(other, GooseGroup):
            other.geese.append(self)
            return other
        return NotImplemented


class WarGoose(Goose):
    def __init__(self, name: str):
        super().__init__(name)
        self.health = 15
        self.damage = 10

    def apply_damage(self, player):
        player.lose_health(self.damage)


class HonkGoose(Goose):
    def __init__(self, name: str):
        super().__init__(name)

    def apply_damage(self, player):
        player.lose_health(self.damage)


class UnluckyGoose(Goose):
    def __init__(self, name: str):
        super().__init__(name)

    def apply_bad_luck(self, player):
        player.lose_luck(self.damage)


class GoldenGoose(Goose):
    def __init__(self, name: str):
        super().__init__(name)

    def return_money(self, player):
        ...
