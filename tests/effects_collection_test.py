from src.infrastructure.collections.effects import EffectsCollection


class FakePlayer:
    def __init__(self, health: int = 100, luck: int = 10):
        self.health = health
        self.luck = luck

    def increase_luck(self, amount: int):
        self.luck += amount

    def lose_health(self, amount: int):
        self.health -= amount


def test_add_and_repr_and_get_power_and_has_effect():
    # Prepare
    p = FakePlayer()
    ec = EffectsCollection(p)

    # Action
    ec.add("honk_damage", 2, 5)

    # Check
    assert ec.has_effect("honk_damage") is True
    assert ec.get_effect_power("honk_damage") == 5
    assert "honk_damage(2st, power:5)" in repr(ec)


def test_bad_luck_behavior_on_readd():
    # Prepare
    p = FakePlayer(luck=10)
    ec = EffectsCollection(p)

    # Action and Check
    ec.add("bad_luck", 3, 4)
    assert ec.get_effect_power("bad_luck") == 4

    ec.add("bad_luck", 1, 7)
    assert p.luck == 14
    assert ec.get_effect_power("bad_luck") == 7


def test_make_step_applies_and_removes():
    # Prepare
    p = FakePlayer(health=20)
    ec = EffectsCollection(p)

    # Action and Check
    ec.add("honk_damage", 1, 6)
    ec.make_step()
    assert p.health == 14
    assert ec.has_effect("honk_damage") is False
    assert repr(ec) == "No effects"


def test_remove_and_get_power_missing():
    # Prepare
    p = FakePlayer()
    ec = EffectsCollection(p)

    # Action and Check
    ec.add("some_effect", 2, 3)
    ec.remove("some_effect")
    assert ec.has_effect("some_effect") is False
    assert ec.get_effect_power("some_effect") == 0
