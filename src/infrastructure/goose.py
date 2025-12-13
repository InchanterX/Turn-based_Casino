from src.infrastructure.player import Player
from random import random


class GooseGroup:
    def __init__(self, geese_list):
        self.geese = geese_list
        self.name = f"Group of {len(geese_list)} geese"

    @property
    def total_health(self):
        """Geese group health in total"""
        return sum(goose.health for goose in self.geese)

    @property
    def total_damage(self):
        """Geese group damage in total"""
        return sum(goose.damage for goose in self.geese)

    @property
    def total_balance(self):
        """Geese group total balance"""
        return sum(goose.balance for goose in self.geese)

    @property
    def steal_amount(self):
        """Geese group steal in total"""
        return sum(goose.steal_amount for goose in self.geese)

    def attack_player(self, player):
        """Attack player with all powers"""
        total_damage = 0
        total_stolen = 0
        effects_applied = []

        for goose in self.geese:
            # Attack
            damage = goose.attack_player(player)
            total_damage += damage

            # Steal
            stolen = goose.steal_from_player(player)
            if stolen > 0:
                total_stolen += stolen
                print(f"💰 {goose.name} stole {stolen} from {player.name}!")

            # record effects
            if isinstance(goose, HonkGoose):
                effects_applied.append("honk")
            elif isinstance(goose, UnluckyGoose):
                effects_applied.append("bad_luck")

        if total_stolen > 0:
            print(
                f"🦢🦢 Group {self.name} dealt {total_damage} damage and stole {total_stolen} total!")
        else:
            print(f"🦢🦢 Group {self.name} dealt {total_damage} damage!")

        return total_damage

    def __repr__(self):
        goose_names = ", ".join(goose.name for goose in self.geese)
        return f"GooseGroup['{self.name}': {goose_names}]"


class Goose:
    '''Default Goose class that define goose stats'''

    def __init__(self, name: str):
        self.name = name
        self.health = 20
        self.damage = 5
        self.balance = 0
        self.steal_amount = 10

    def attack_player(self, player):
        """Just heat a player"""
        player.lose_health(self.damage)
        print(f"🦢 {self.name} hit {player.name} for {self.damage}HP!")
        return self.damage

    def steal_from_player(self, player):
        """Steal money from player if it possible"""
        if self.steal_amount <= 0:
            return 0

        if player.get_chips_value() >= self.steal_amount:
            if player.lesion(self.steal_amount):
                self.balance += self.steal_amount
                return self.steal_amount
        return 0

    def __add__(self, other):
        if isinstance(other, Goose):
            return GooseGroup([self, other])
        elif isinstance(other, GooseGroup):
            other.geese.append(self)
            return other
        return NotImplemented

    def __repr__(self):
        return f"Goose('{self.name}', HP={self.health}, DMG={self.damage}, STEAL={self.steal_amount})"


class WarGoose(Goose):
    def __init__(self, name: str):
        super().__init__(name)
        self.health = 15
        self.damage = 10
        self.critical_chance = 0.3
        self.steal_amount = 5

    def attack_player(self, player):
        """Hit player with a possibility of dealing crit damage"""

        crit_damage = self.damage
        if random() < self.critical_chance:
            crit_damage = int(self.damage * 2)
            print(f"💥 Goose {self.name} hit you with crit damage!")

        player.lose_health(crit_damage)
        print(f"⚔️ {self.name} hit {player.name} for {crit_damage}HP!")
        return crit_damage

    def __repr__(self):
        return f"WarGoose('{self.name}', HP={self.health}, DMG={self.damage}, STEAL={self.steal_amount}, CRIT={self.critical_chance})"


class HonkGoose(Goose):
    def __init__(self, name: str):
        super().__init__(name)
        self.damage = 3
        self.steal_amount = 7

    def attack_player(self, player):
        """Goose's honk apply long damage for 3 steps"""
        player.effects.add("honk_damage", duration=3, power=self.damage)
        print(
            f"📢 {self.name} honked on {player.name}! Applied honk damage status for 3 steps!")
        return self.damage

    def __repr__(self):
        return f"HonkGoose('{self.name}', HP={self.health}, DMG={self.damage}, STEAL={self.steal_amount})"


class UnluckyGoose(Goose):
    def __init__(self, name: str):
        super().__init__(name)
        self.bad_luck_power = 12
        self.health = 18
        self.steal_amount = 10

    def attack_player(self, player):
        """Apply unlucky effect for 5 steps"""
        player.effects.add("bad_luck", duration=5, power=self.bad_luck_power)
        player.decrease_luck(self.bad_luck_power)
        print(
            f"☠️ Goose {self.name} cursed {player.name} with bad luck! -{self.bad_luck_power} units of luck for the next five steps!")
        return self.damage

    def __repr__(self):
        return f"UnluckyGoose('{self.name}', HP={self.health}, STEAL={self.steal_amount}, BAD_LUCK={self.bad_luck_power})"


class GoldenGoose(Goose):
    def __init__(self, name: str):
        super().__init__(name)
        self.health = 25
        self.money_multiplier = 0.5
        self.steal_amount = 0

    def attack_player(self, player):
        """Gather some percent of money from other geese according to money_multiplier"""
        total_collected = 0
        geese_robbed = []

        for goose in geese_collection:
            if goose != self and goose.balance > 0:
                collected = int(goose.balance * self.gold_multiplier)
                goose.balance -= collected
                self.balance += collected
                total_collected += collected
                geese_robbed.append(goose.name)

        if geese_robbed:
            print(
                f"💰 {self.name} collected {total_collected} from geese: {', '.join(geese_robbed)}")

        return total_collected

    def __repr__(self):
        return f"GoldenGoose('{self.name}', HP={self.health}, DMG={self.damage}, STEAL={self.steal_amount}, MULT={self.money_multiplier})"
