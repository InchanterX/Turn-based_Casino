class EffectsCollection:
    def __init__(self):
        self._effects = {}

    def add(self, effect: str, duration: int, power: int):
        '''Add effect to the list of active effects. If such effect already exist strengthen or/and prolong it.'''
        if effect in self._effects:
            old_duration, old_power = self._effects[effect]
            new_duration = max(old_duration, duration)
            new_power = max(old_power, power)
            self._effects[effect] = [new_duration, new_power]
        else:
            self._effects[effect] = [duration, power]

    def remove(self, effect: str):
        '''Remove effect from the list of effects'''
        if effect in self._effects:
            del self._effects[effect]

    def make_step(self):
        '''Make step and decrease duration of all effects by one'''
        for key in self._effects.keys():
            self._effects[key][0] -= 1
        self._audit_of_effects()

    def _audit_of_effects(self):
        '''Check if effects are still going'''
        for key in self._effects.keys():
            if self._effects[key] <= 0:
                self.remove(self._effects[key])

    def has_effect(self, effect: str) -> bool:
        """Check if were is such effect"""
        return effect in self._effects

    def get_effect_power(self, effect: str) -> int:
        """Return effect power or 0"""
        if effect in self._effects:
            return self._effects[effect][1]
        return 0

    def __repr__(self) -> str:
        if not self._effects:
            return "No effects"
        effects_str = []
        for name, (duration, power) in self._effects.items():
            effects_str.append(f"{name}({duration}st, power:{power})")
        return ", ".join(effects_str)
