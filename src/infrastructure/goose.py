from random import random


class GooseGroup:
    def __init__(self, geese_list):
        self.geese = geese_list
        self.name = f"Group of {len(geese_list)} geese"

    @property
    def alive_geese(self):
        """Get list of alive geese"""
        return [goose for goose in self.geese if goose.is_alive()]

    def remove_dead_geese(self):
        """Remove dead geese from group"""
        initial_count = len(self.geese)
        self.geese = self.alive_geese

        if len(self.geese) < initial_count:
            dead_count = initial_count - len(self.geese)
            print(f"[💀] {dead_count} geese from group had died {self.name}!")

            if self.geese:
                self.name = f"Group of {len(self.geese)} geese"
            else:
                self.name = "Empty group (all dead)"

    @property
    def total_health(self):
        """Geese group health in total (only alive)"""
        return sum(goose.health for goose in self.alive_geese)

    @property
    def total_damage(self):
        """Geese group damage in total (only alive)"""
        return sum(goose.damage for goose in self.alive_geese)

    @property
    def total_balance(self):
        """
        Geese group total balance (all geese, including dead).
        Saved for Golden Goose
        """
        return sum(goose.balance for goose in self.geese)

    @property
    def total_alive_balance(self):
        """Geese group balance of alive geese only"""
        return sum(goose.balance for goose in self.alive_geese)

    @property
    def steal_amount(self):
        """Geese group steal in total (only alive)"""
        return sum(goose.steal_amount for goose in self.alive_geese)

    @property
    def is_alive(self) -> bool:
        """Check if any goose in group is alive"""
        return any(goose.is_alive() for goose in self.geese)

    def attack_player(self, player, damage_multiplier: int = 1):
        """Attack player with all powers"""
        had_dead = self.remove_dead_geese()

        # No goose alive
        if not self.is_alive:
            print(
                f"🦢 Group is unable to attack {self.name} - everyone is dead!")

        if had_dead:
            print(f"🦢 {len(self.geese)} geese left in group")

        total_damage = 0
        total_stolen = 0
        effects_applied = []

        for goose in self.alive_geese:
            if isinstance(goose, GoldenGoose):
                damage = goose.attack_player(player, damage_multiplier, [self])
            else:
                damage = goose.attack_player(player, damage_multiplier)

            total_damage += damage

            print(f"🦢🦢 Group {self.name} dealt {total_damage} damage!")

        # remove extra
        unique_effects = set(effects_applied)
        if unique_effects:
            print(f"⚡ Примененные эффекты: {', '.join(unique_effects)}")

        return total_damage, total_stolen

    def steal_from_player(self, player):
        """Group steal one by one"""
        total_stolen = 0
        for goose in self.alive_geese:
            stolen = goose.steal_from_player(player)
            if stolen > 0:
                total_stolen += stolen
                print(f"💰 {goose.name} украл {stolen} у {player.name}")

        if total_stolen > 0:
            print(f"🦢🦢 Группа {self.name} украла {total_stolen} всего!")

        return total_stolen

    def __add__(self, other):
        """Unite geese"""
        if isinstance(other, Goose):
            self.geese.append(other)
            self.name = f"Group of {len(self.geese)} geese"
            print(f"🦢 {other.name} присоединился к группе {self.name}")
            return self
        elif isinstance(other, GooseGroup):
            self.geese.extend(other.geese)
            self.name = f"Group of {len(self.geese)} geese"
            print(f"🦢🦢 Группы объединились в {self.name}")
            return self
        return NotImplemented

    def __repr__(self):
        if not self.geese:
            return "GooseGroup[Empty]"

        alive_count = len(self.alive_geese)
        dead_count = len(self.geese) - alive_count

        goose_info = []
        for goose in self.geese:
            status = "💀" if not goose.is_alive() else "❤️"
            goose_info.append(f"{status}{goose.name}({goose.health}HP)")

        return f"GooseGroup['{self.name}': {', '.join(goose_info)} | 🎯{self.total_damage} ⚡{self.steal_amount} 💰{self.total_balance}]"


class Goose:
    '''Default Goose class that define goose stats'''

    def __init__(self, name: str):
        self.name = name
        self.health = 20
        self.damage = 5
        self.balance = 0
        self.steal_amount = 10

    def is_alive(self) -> bool:
        '''Check if goose is alive'''
        return self.health > 0

    def lose_health(self, amount: int):
        '''Reduce goose health'''
        self.health = max(0, self.health - amount)
        if amount > 0:
            print(
                f"[🦢] Goose {self.name} lost {amount} HP! ({self.health} HP left)")

    def attack_player(self, player, damage_multiplier: int, goose_collection=None):
        """Heat a player with a possibility of parring"""
        base_damage = self.damage

        if damage_multiplier >= 1:
            actual_damage = max(1, base_damage // damage_multiplier)
        else:
            actual_damage = base_damage

        player.lose_health(actual_damage)
        print(f"🦢 {self.name} hit player {player.name} for {actual_damage}HP!")

        if damage_multiplier >= 4:
            parry_ratio = (damage_multiplier - 3) / 3
            reflected_damage = int(actual_damage * parry_ratio)

            if reflected_damage > 0:
                self.lose_health(reflected_damage)
                print(
                    f"⚔️ {player.name} parried attack! {self.name} lost {reflected_damage}HP!")

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

    def attack_player(self, player, damage_multiplier: int):
        """Hit player with a possibility of dealing crit damage"""
        base_damage = self.damage

        # crit damage
        crit_damage = self.damage
        if random() < self.critical_chance:
            crit_damage = int(self.damage * 2)
            print(f"💥 Goose {self.name} hit you with crit damage!")

        if damage_multiplier >= 1:
            actual_damage = max(1, base_damage // damage_multiplier)
        else:
            actual_damage = base_damage

        player.lose_health(actual_damage)
        print(f"⚔️ {self.name} hit {player.name} for {actual_damage}HP!")

        if damage_multiplier >= 4:
            parry_ratio = (damage_multiplier - 3) / 3
            reflected_damage = int(actual_damage * parry_ratio)

            if reflected_damage > 0:
                self.lose_health(reflected_damage)
                print(
                    f"⚔️ Player {player.name} parried attack! {self.name} lost {reflected_damage}HP!")

    def __repr__(self):
        return f"WarGoose('{self.name}', HP={self.health}, DMG={self.damage}, STEAL={self.steal_amount}, CRIT={self.critical_chance})"


class HonkGoose(Goose):
    def __init__(self, name: str):
        super().__init__(name)
        self.damage = 3
        self.steal_amount = 7

    def attack_player(self, player, damage_multiplier: int = 1):
        """Goose's honk apply long damage for 3 steps"""
        player.effects.add("honk_damage", duration=3, power=self.damage)
        print(
            f"📢 {self.name} honked on {player.name}! Applied honk damage status for 3 steps!")

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

    def __repr__(self):
        return f"UnluckyGoose('{self.name}', HP={self.health}, STEAL={self.steal_amount}, BAD_LUCK={self.bad_luck_power})"


class GoldenGoose(Goose):
    def __init__(self, name: str):
        super().__init__(name)
        self.health = 25
        self.money_multiplier = 0.5
        self.steal_amount = 0

    def attack_player(self, player, goose_collection=None):
        """Gather some percent of money from other geese according to money_multiplier"""
        total_collected = 0

        if goose_collection:
            geese_robbed = []
            for goose in goose_collection:
                if goose != self and goose.balance > 0:
                    collected = int(goose.balance * self.money_multiplier)
                    # prevent negative balance
                    collected = min(collected, goose.balance)
                    goose.balance -= collected
                    self.balance += collected
                    total_collected += collected
                    geese_robbed.append(f"{goose.name}(-{collected})")

            if geese_robbed:
                print(
                    f"💰 {self.name} collected {total_collected} from: {', '.join(geese_robbed)}")

        # reduced_damage = max(1, self.damage // 2)
        # player.lose_health(reduced_damage)
        # print(f"🦢 {self.name} hit {player.name} for {reduced_damage}HP!")

        if total_collected > 0:
            bonus = total_collected // 4  # 25%
            player.chips_income(bonus)
            print(f"💰 {self.name} shared {bonus} with {player.name}!")

        return total_collected  # Возвращаем сколько собрали

    def collect_from_geese(self, goose_collection):
        """Отдельный метод для сбора денег без атаки игрока"""
        total = 0
        for goose in goose_collection:
            if goose != self and goose.balance > 0:
                collected = int(goose.balance * self.money_multiplier)
                collected = min(collected, goose.balance)
                goose.balance -= collected
                self.balance += collected
                total += collected
        return total

    def __repr__(self):
        return f"GoldenGoose('{self.name}', HP={self.health}, BAL={self.balance}, MULT={self.money_multiplier})"
