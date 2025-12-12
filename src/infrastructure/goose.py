from src.infrastructure.player import Player


class Goose:
    '''
    Default Goose class that define goose stats
    '''

    def __init__(self, name):
        self.name = name
        self.health = 20
        self.damage = 5
        self.balance = 0


class WarGoose(Goose):
    def __init__(self):
        super(Goose, self).__init__()
        self.health = 15
        self.damage = 10

    def apply_damage(self, player):
        player.lose_health(self.damage)


class HonkGoose(Goose):
    def __init__(self):
        super(Goose, self).__init__()

    def apply_damage(self, player):
        player.lose_health(self.damage)


class UnluckyGoose(Goose):
    def __init__(self):
        super(Goose, self).__init__()

    def apply_bad_luck(self, player):
        player.lose_luck(self.damage)


class GoldenGoose(Goose):
    def __init__(self):
        super(Goose, self).__init__()

    def return_money(self, player):
        ...
