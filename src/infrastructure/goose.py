from src.infrastructure.logger import logger
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
                f"[🦢] Group is unable to attack {self.name} - everyone is dead!")

        if had_dead:
            print(f"[🦢] {len(self.geese)} geese left in group")

        total_damage = 0
        total_stolen = 0
        # effects_applied = []

        for goose in self.alive_geese:
            if isinstance(goose, GoldenGoose):
                damage = goose.attack_player(player, damage_multiplier, [self])
            else:
                damage = goose.attack_player(player, damage_multiplier)

            total_damage += damage

        print(f"[🦢🦢] {self.name} dealt {total_damage} damage in total!")

        # remove extra
        # unique_effects = set(effects_applied)
        # if unique_effects:
        #     print(f"[⚡] Apply effects: {', '.join(unique_effects)}")

        return total_damage, total_stolen

    def steal_from_player(self, player):
        """Group steal one by one"""
        total_stolen = 0
        for goose in self.alive_geese:
            stolen = goose.steal_from_player(player)
            if stolen > 0:
                total_stolen += stolen
                # print(f"[💰] {goose.name} stole {stolen} from {player.name}")

        if total_stolen > 0:
            print(
                f"[🦢🦢] {self.name} totally stole {total_stolen} from player {player.name}!")

        return total_stolen

    def __add__(self, other):
        """Unite geese"""
        if isinstance(other, Goose):
            self.geese.append(other)
            self.name = f"Group of {len(self.geese)} geese"
            logger.info(f"{other.name} united with {self.name} to group.")
            print(f"[🦢] {other.name} united with {self.name}.")
            return self
        elif isinstance(other, GooseGroup):
            self.geese.extend(other.geese)
            self.name = f"Group of {len(self.geese)} geese"
            logger.info(
                f"{other.name} united with {self.name} to a new group.")
            print(f"[🦢🦢]: Groups united to {self.name}")
            return self
        return NotImplemented

    def __repr__(self):
        if not self.geese:
            return "GooseGroup[Empty]"

        # alive_count = len(self.alive_geese)
        # dead_count = len(self.geese) - alive_count

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
        self.steal_amount = 30

    def is_alive(self) -> bool:
        '''Check if goose is alive'''
        return self.health > 0

    def lose_health(self, amount: int):
        '''Reduce goose health'''
        self.health = max(0, self.health - amount)
        if amount > 0:
            print(
                f"[🦢]: Goose {self.name} lost {amount} HP! ({self.health} HP left)")

    def attack_player(self, player, damage_multiplier: int, goose_collection=None) -> int:
        """Heat a player with a possibility of parring"""
        base_damage = self.damage

        if damage_multiplier >= 1 and damage_multiplier <= 3:
            actual_damage = max(1, base_damage // damage_multiplier)
        elif damage_multiplier >= 4:
            actual_damage = 0
            reduction_ratio = 1.0 / (7 - damage_multiplier)
            parry_damage = max(1, int(base_damage * reduction_ratio))
        else:
            actual_damage = base_damage

        if actual_damage <= 0:
            print(f"[⚔️]: {self.name} failed to hit {player.name}!")
        else:
            player.lose_health(actual_damage)
            print(
                f"[⚔️]: {self.name} hit {player.name} for {actual_damage}HP!")

        if damage_multiplier >= 4:
            if parry_damage > 0:
                self.lose_health(parry_damage)
                print(
                    f"[⚔️]: Player {player.name} parried attack! {self.name} lost {parry_damage}HP!")
        return actual_damage

    def steal_from_player(self, player) -> int:
        """Steal money from player if it possible"""
        if self.steal_amount <= 0:
            logger.info(f"Goose {self.name} doesn't have enough steal power.")
            print(f"[🦢 Steal]: {self.name} have a skill issue.")
            return 0

        if player.get_chips_value() >= self.steal_amount:
            # if player.chips_lesion(self.steal_amount):
            player.chips_lesion(self.steal_amount)
            self.balance += self.steal_amount
            logger.info(
                f"Goose {self.name} stole {self.steal_amount} chips from player {player.name}.")
            print(
                f"[💰 Steal]: {self.name} stole {self.steal_amount} chips from {player.name}.")
            return self.steal_amount
        elif player.balance >= self.steal_amount:
            # if player.balance_lesion(self.steal_amount):
            player.balance_lesion(self.steal_amount)
            self.balance += self.steal_amount
            logger.info(
                f"Goose {self.name} stole {self.steal_amount} money from player {player.name}.")
            print(
                f"[💰 Steal]: {self.name} stole {self.steal_amount} money from {player.name}.")
            return self.steal_amount
        logger.info(
            f"Goose {self.name} wanted to stile from player {player.name} but player is poor.")
        print(
            f"[💰 Steal]: {self.name} wanted to stile from {player.name} but player is poor.")
        return 0

    def __add__(self, other):
        if isinstance(other, Goose):
            logger.info(f"{other.name} united with {self.name} to group.")
            print(f"[🦢] {other.name} united with {self.name}.")
            return GooseGroup([self, other])
        elif isinstance(other, GooseGroup):
            logger.info(f"{other.name} united with {self.name} to group.")
            print(f"[🦢] {other.name} united with {self.name}.")
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
        self.steal_amount = 20

    def attack_player(self, player, damage_multiplier: int, goose_collection=None) -> int:
        """Hit player with a possibility of dealing crit damage"""
        base_damage = self.damage

        # crit damage
        is_critical = random() < self.critical_chance
        if is_critical:
            base_damage = int(self.damage * 2)

        if damage_multiplier >= 1 and damage_multiplier <= 3:
            actual_damage = max(1, base_damage // damage_multiplier)
        elif damage_multiplier >= 4:
            actual_damage = 0
            reduction_ratio = 1.0 / (damage_multiplier - 2)
            parry_damage = max(1, int(base_damage * reduction_ratio))
        else:
            actual_damage = base_damage

        if actual_damage <= 0:
            print(f"[⚔️]: {self.name} failed to hit {player.name}!")
        elif is_critical:
            print(
                f"[💥]: Goose {self.name} hit you with {actual_damage} crit damage!")
        else:
            player.lose_health(actual_damage)
            print(
                f"[⚔️]: {self.name} hit {player.name} for {actual_damage}HP!")

        if damage_multiplier >= 4:
            if parry_damage > 0:
                self.lose_health(parry_damage)
                print(
                    f"[⚔️]: Player {player.name} parried attack! {self.name} lost {parry_damage}HP!")
        return actual_damage

    def __repr__(self):
        return f"WarGoose('{self.name}', HP={self.health}, DMG={self.damage}, STEAL={self.steal_amount}, CRIT={self.critical_chance})"


class HonkGoose(Goose):
    def __init__(self, name: str):
        super().__init__(name)
        self.damage = 3
        self.steal_amount = 25

    def attack_player(self, player, damage_multiplier: int = 1, goose_collection=None) -> int:
        """Goose's honk apply long damage for 3 steps"""
        player.effects.add("honk_damage", duration=3, power=self.damage)
        print(
            f"[📢]: {self.name} honked on {player.name}! Applied honk damage status for 3 steps!")
        return 0

    def __repr__(self):
        return f"HonkGoose('{self.name}', HP={self.health}, DMG={self.damage}, STEAL={self.steal_amount})"


class UnluckyGoose(Goose):
    def __init__(self, name: str):
        super().__init__(name)
        self.bad_luck_power = 12
        self.health = 18
        self.steal_amount = 40

    def attack_player(self, player, damage_multiplier: int = 1, goose_collection=None) -> int:
        """Apply unlucky effect for 5 steps"""
        player.effects.add("bad_luck", duration=5, power=self.bad_luck_power)
        player.decrease_luck(self.bad_luck_power)
        print(
            f"[☠️]: Goose {self.name} cursed {player.name} with bad luck! -{self.bad_luck_power} units of luck for the next five steps!")
        return 0

    def __repr__(self):
        return f"UnluckyGoose('{self.name}', HP={self.health}, STEAL={self.steal_amount}, BAD_LUCK={self.bad_luck_power})"


class GoldenGoose(Goose):
    def __init__(self, name: str):
        super().__init__(name)
        self.health = 25
        self.money_multiplier = 0.5
        self.steal_amount = 0

    def attack_player(self, player, damage_multiplier: int = 1, goose_collection=None) -> int:
        """Collect money from all other geese"""
        total = 0
        for goose in goose_collection:
            if goose == self:
                continue

            if isinstance(goose, GooseGroup):
                current_balance = goose.total_balance
                if current_balance <= 0:
                    continue

                collected = int(current_balance * self.money_multiplier)
                collected = min(collected, current_balance)

                self._collect_from_group(goose, collected)
            else:
                if goose.balance <= 0:
                    continue

                collected = int(goose.balance * self.money_multiplier)
                collected = min(collected, goose.balance)
                goose.balance -= collected

            total += collected

        self.balance += total//2
        player.chips_income(total//2)

        return 0

    def _collect_from_group(self, group, amount):
        """Gather money from group in proportion"""
        if not group.geese or amount <= 0:
            return

        total_group_balance = group.total_balance
        if total_group_balance <= 0:
            return
        remaining_amount = amount

        for goose in group.geese:
            if goose.balance <= 0 or remaining_amount <= 0:
                continue

            # Gather part
            goose_share = int((goose.balance / total_group_balance) * amount)
            goose_share = min(goose_share, goose.balance, remaining_amount)

            goose.balance -= goose_share
            remaining_amount -= goose_share

        # Take everything that remained from the first goose
        if remaining_amount > 0 and group.geese:
            first_goose = group.geese[0]
            if first_goose.balance >= remaining_amount:
                first_goose.balance -= remaining_amount

    def __repr__(self):
        return f"GoldenGoose('{self.name}', HP={self.health}, BAL={self.balance}, MULT={self.money_multiplier})"
