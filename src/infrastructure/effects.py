class EffectsCollection:
    def __init__(self):
        self._effects = {}

    def add(self, effect, duration):
        if self._effects[effect]:
            self._effects[effect] = max(self._effects[effect], duration)
        else:
            self._effects[effect] = duration

    def remove(self, type):
        ...

    def proceed(self):
        ...
