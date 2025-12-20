from src.infrastructure.logger import logger


class EffectsCollection:
    def __init__(self, player):
        self._effects = {}
        self.player = player

    def add(self, effect: str, duration: int, power: int):
        '''Add effect to the list of active effects. If such effect already exist strengthen or/and prolong it.'''
        if effect in self._effects:
            old_duration, old_power = self._effects[effect]
            new_duration = max(old_duration, duration)
            if effect == "bad_luck":
                self.player.increase_luck(old_power)
                new_power = power
                new_duration = duration
            else:
                new_power = max(old_power, power)
            self._effects[effect] = [new_duration, new_power]
            logger.info(
                f"Effect {effect} was updated to duration {new_duration} and power {new_power}.")
        else:
            self._effects[effect] = [duration, power]
            logger.info(
                f"Effect {effect} was added with duration {duration} and power {power}.")

    def remove(self, effect: str):
        '''Remove effect from the list of effects'''
        if effect in self._effects.keys():
            del self._effects[effect]
            logger.info(
                f"Effect {effect} was removed.")

    def make_step(self):
        '''Make step and decrease duration of all effects by one'''
        self._apply_effects()
        for key in self._effects.keys():
            self._effects[key][0] -= 1
        self._audit_of_effects()
        logger.info("Made a step in effects collection.")

    def _apply_effects(self):
        '''Apply effects that currently applied'''
        for key in self._effects.keys():
            power = self.get_effect_power(key)
            if key == "honk_damage":
                self.player.lose_health(power)
                logger.info(
                    f"Honk damage of {power} was applied to player {self.player.name}.")
                print(
                    f"Honk damage was applied ({self._effects[key][0]} steps left)")

    def _audit_of_effects(self):
        '''Check if effects are still going'''
        keys_to_remove = []
        for key, (duration, power) in self._effects.items():
            if duration <= 0:
                if key == "bad_luck":
                    self.player.increase_luck(power)
                keys_to_remove.append(key)

        for key in keys_to_remove:
            logger.info(f"Effect {key} has expired and will be removed.")
            self.remove(key)

    def has_effect(self, effect: str) -> bool:
        """Check if were is such effect"""
        logger.info(f"Checked for effect {effect}.")
        return effect in self._effects

    def get_effect_power(self, effect: str) -> int:
        """Return effect power or 0"""
        if effect in self._effects:
            logger.info(
                f"Returning power of effect {effect}: {self._effects[effect][1]}"
            )
            return self._effects[effect][1]
        logger.info(f"Effect {effect} not found. Returning 0 power.")
        return 0

    def __repr__(self) -> str:
        if not self._effects:
            return "No effects"
        effects_str = []
        for name, (duration, power) in self._effects.items():
            effects_str.append(f"{name}({duration}st, power:{power})")
        return ", ".join(effects_str)
