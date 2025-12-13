from src.infrastructure.logger import logger
from src.infrastructure.constants import ADVERTISEMENTS
from random import choice, randint


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
            return f"🎰 {player.name} wanted to bet {bet_amount} but is broke!"

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
            return "🦢 No players or geese for attack"

        # check if goose can apply damage
        if hasattr(goose, 'apply_damage'):
            # chosen goose is WarGoose or HonkGoose
            goose.apply_damage(player)
        else:
            # Обычный гусь
            player.lose_health(goose.damage)

        logger.info(f"Goose {goose.name} attacked {player.name}")
        return f"🦢 ATTACK: {goose.name} attacked {player.name} for {goose.damage} damage!"

    def goose_steal_event(self) -> str:
        '''Goose steals money from player'''
        player = self._random_player()
        goose = self._random_goose()

        if player is None or goose is None:
            return "💰 No players or geese for stealing"

        # Сумма кражи от 5 до 50 или 10% от баланса
        max_steal = min(50, player.get_chips_value() // 10)
        if max_steal < 5:
            return f"💰 {goose.name} tried to steal from {player.name} but they're too poor!"

        steal_amount = randint(5, max_steal)

        if player.lesion(steal_amount):
            goose.balance += steal_amount
            logger.info(
                f"Goose {goose.name} stole {steal_amount} from {player.name}")

            # Проверяем, не GoldenGoose ли это
            if hasattr(goose, 'return_money'):
                # GoldenGoose возвращает часть денег
                returned = goose.return_money(player, steal_amount)
                return f"💰 STEAL & RETURN: {goose.name} stole {steal_amount} but returned {returned} to {player.name}!"
            else:
                return f"💰 STEAL: {goose.name} stole {steal_amount} from {player.name}!"
        else:
            return f"💰 STEAL FAILED: {goose.name} failed to steal from {player.name}!"

    def geese_unite_event(self):
        if len(self.casino.geese) >= 2:
            goose1 = choice(self.casino.geese)
            goose2 = choice([goose for goose in self.casino.geese])

            group = goose1 + goose2
            self.casino.geese.remove(goose1)
            self.casino.geese.remove(goose2)
            self.casino.geese.append(group)
            print(f"Geese {goose1} and {goose2} gathered to group!")

    def golden_goose_event(self) -> str:
        '''Golden goose bonus event'''
        # Ищем GoldenGoose в коллекции
        golden_geese = [
            g for g in self.casino.geese if hasattr(g, 'return_money')]

        if not golden_geese:
            # Если нет GoldenGoose, создаём одного
            from src.infrastructure.goose import GoldenGoose
            golden_goose = GoldenGoose("Lucky Goldie")
            self.casino.geese.append(golden_goose)
            logger.info(f"Created new GoldenGoose: {golden_goose.name}")
            return f"💰 GOLDEN GOOSE: A new Golden Goose '{golden_goose.name}' appeared!"

        # Если есть GoldenGoose, даём бонус игроку
        player = self._random_player()
        if player is None:
            return "💰 No players for golden goose bonus"

        golden_goose = choice(golden_geese)
        bonus_amount = randint(50, 200)

        # GoldenGoose возвращает деньги (имитация кражи + возврат)
        stolen = bonus_amount * 2  # Представляем, что украли в 2 раза больше
        returned = golden_goose.return_money(player, stolen)

        logger.info(
            f"Golden goose {golden_goose.name} gave {returned} to {player.name}")
        return f"💰 GOLDEN BONUS: {golden_goose.name} blessed {player.name} with {returned}!"
