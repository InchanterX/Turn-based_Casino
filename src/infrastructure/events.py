from src.infrastructure.logger import logger
from src.infrastructure.constants import ADVERTISEMENTS
from random import choice, randint, random
from src.infrastructure.goose import GoldenGoose


class Events:
    def __init__(self, casino):
        self._logger = logger
        self.casino = casino

        # list of available events with possibilities
        self.events = [
            ("player_bet", 60, self.player_bet_event),
            ("goose_attack", 20, self.goose_attack_event),
            ("goose_steal", 15, self.goose_steal_event),
            ("geese_unite", 10, self.geese_unite_event),
            ("advertisement_break", 30, self.advertisement_event),
            ("stroke", 5, self.stroke_event),
            ("golden_goose_bonus", 5, self.golden_goose_event),
            # ("lucky_win", 5, self.lucky_win_event)
        ]

    def _random_player(self):
        '''
        Select random player from the list.
        In default implementation there is only one player, so it will always chose it.
        '''
        if len(self.casino.players) == 0:
            return None
        return choice(self.casino.players)

    def _random_goose(self):
        '''
        Select random goose from the list.
        '''
        if len(self.casino.geese) == 0:
            return None
        return choice(self.casino.geese)

    def get_random_event(self):
        '''Chose random event from the list by their weight'''
        total = sum(possibility for _, possibility, _ in self.events)
        result = randint(1, total)
        current = 0

        for name, possibility, function in self.events:
            current += possibility
            if result <= current:
                return function

        # in case of exception
        return self.events[0][2]

    def advertisement_event(self) -> str:
        '''Print advertisement to the CLI'''
        logger.info(
            f"Displayed advertisement to the player.")
        return f"[📺 Adv] {choice(ADVERTISEMENTS)}"

    def stroke_event(self) -> bool:
        '''Hit player with stroke'''
        player = self._random_player()
        player.lose_health(100)
        logger.info(
            f"Player {player.name} has died from the stroke.")
        print(
            f"[💀 Stroke] Player {player.name} has died because of stroke! How unfortunately...")
        return True

    def player_bet_event(self) -> str:
        '''Event of player making a bet'''
        player = self._random_player()
        if player is None:
            logger.warning("No players to place bets.")
            return "No players to place bets!"

        max_bet = max(10, player.get_chips_value() // 10)
        bet_amount = randint(10, max_bet)

        if player.get_chips_value() < bet_amount:
            return f"[🎰] {player.name} wanted to bet {bet_amount} but is broke!"

        # 45% шанс выигрыша, 55% проигрыша (казино должно выигрывать)
        if random() < 0.45:
            # Выигрыш: от 1.5x до 3x
            multiplier = random() * 1.5 + 1.5  # 1.5 - 3.0
            win_amount = int(bet_amount * multiplier)
            player.income(win_amount)
            logger.info(
                f"Player {player.name} won {win_amount} from bet {bet_amount}")
            return f"🎰 BET WIN: {player.name} bet {bet_amount} and won {win_amount}!"
        else:
            # Проигрыш
            player.lesion(bet_amount)
            logger.info(f"Player {player.name} lost {bet_amount} in bet")
            return f"🎰 BET LOSS: {player.name} lost {bet_amount} in a bet!"

    def goose_attack_event(self) -> str:
        '''Goose attacks a player'''
        player = self._random_player()
        goose = self._random_goose()

        if player is None or goose is None:
            return "[🦢 Goose] No players or geese for attack"

        # Attack
        damage = goose.attack_player(player)

        # Stole prepare
        stolen = 0
        if hasattr(goose, 'steal_from_player'):
            stolen = goose.steal_from_player(player)

        # Golden goose case
        collected_from_geese = 0
        if hasattr(goose, 'collect_from_geese'):
            collected_from_geese = goose.collect_from_geese(self.casino.geese)

        message_parts = []
        message_parts.append(
            f"[🦢 Goose] {goose.name} attacked {player.name} for {damage} damage!")

        if stolen > 0:
            message_parts.append(f"stole {stolen}")

        if collected_from_geese > 0:
            message_parts.append(
                f"collected {collected_from_geese} from other geese")

        return " | ".join(message_parts)

    def goose_steal_event(self) -> str:
        '''Goose steals money from player'''
        player = self._random_player()
        goose = self._random_goose()

        if player is None or goose is None:
            return "[💰 Steal]: No players or geese for stealing"

        # Actually steal
        if hasattr(goose, 'steal_from_player'):
            stolen = goose.steal_from_player(player)
            if stolen > 0:
                logger.info(
                    f"Goose {goose.name} stole {stolen} from {player.name}")

                # Additional effects for UnluckyGoose
                if goose.__class__.__name__ == "UnluckyGoose":
                    luck_reduction = stolen // 2
                    player.decrease_luck(luck_reduction)
                    player.effects.add(
                        "bad_luck", duration=3, power=luck_reduction)
                    return f"[💰☠️ Curse]: {goose.name} stole {stolen} and cursed {player.name}'s luck (-{luck_reduction})!"

                return f"[💰 Steal]: {goose.name} stole {stolen} from {player.name}!"
            else:
                return f"[💰 Steal]: {goose.name} failed to steal from {player.name}!"
        else:
            return f"[💰 Steal]: {goose.name} doesn't know how to steal!"

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

    def golden_goose_event(self) -> str:
        '''Golden goose gives bonus money to player by steeling them from other'''
        golden_geese = [
            goose for goose in self.casino.geese
            if isinstance(goose, GoldenGoose)
        ]

        # Create one
        if not golden_geese:
            golden_goose = GoldenGoose("Lucky One")
            self.casino.geese.append(golden_goose)
            logger.info(f"Created new GoldenGoose: {golden_goose.name}")
            return f"[💰 Golden One]: A new Golden Goose '{golden_goose.name}' appeared!"

        # Choose player
        player = self._random_player()
        if player is None:
            return "[💰 Golden One] No players for golden goose bonus"

        # Choose goose
        golden_goose = choice(golden_geese)

        # Calculating bonus
        if golden_goose.balance > 0:
            bonus = golden_goose.balance // 2
            golden_goose.balance -= bonus
            player.income(bonus)
            logger.info(
                f"Golden goose {golden_goose.name} gave {bonus} to {player.name}")
            return f"[💰 Golden Gift]: {golden_goose.name} gave {bonus} to {player.name}!"
        else:
            # No money? Let's steal them
            collected = golden_goose.collect_from_geese(self.casino.geese)
            if collected > 0:
                bonus = collected // 2
                player.income(bonus)
                return f"[💰 Golden Sharing]: {golden_goose.name} collected {collected}, shared {bonus} with {player.name}!"
            else:
                return f"[💰 Golden {golden_goose.name} wanted to help but all geese are broke!"
