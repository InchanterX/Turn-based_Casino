from unittest.mock import Mock, patch
from src.infrastructure.goose import Goose, WarGoose, HonkGoose, UnluckyGoose, GoldenGoose, GooseGroup


class TestGooseSystem:

    def test_goose_basic_mechanics(self):
        # Prepare
        goose = Goose("Alpha")

        # Action
        goose.lose_health(5)
        is_alive_before = goose.is_alive()
        goose.lose_health(20)
        is_alive_after = goose.is_alive()

        # Check
        assert goose.health == 0
        assert is_alive_before is True
        assert is_alive_after is False

    def test_goose_attack_and_parry(self):
        # Prepare
        goose = Goose("Fighter")
        player = Mock()

        # Action
        goose.attack_player(player, damage_multiplier=1)
        goose.attack_player(player, damage_multiplier=5)

        # Check
        assert player.lose_health.called
        assert goose.health < 20

    def test_goose_steal_logic(self):
        # Prepare
        goose = Goose("Thief")
        player = Mock()
        player.name = "Bob"
        player.get_chips_value.return_value = 100

        # Action
        stolen_chips = goose.steal_from_player(player)

        # Check
        assert stolen_chips == 30
        player.chips_lesion.assert_called_with(30)
        assert goose.balance == 30

    def test_war_goose_critical_hit(self):
        # Prepare
        war_goose = WarGoose("Soldier")
        player = Mock()

        # Action and Check
        with patch('src.infrastructure.goose.random', return_value=0.1):
            damage = war_goose.attack_player(player, 1)
            assert damage == 20

        with patch('src.infrastructure.goose.random', return_value=0.9):
            damage = war_goose.attack_player(player, 1)
            assert damage == 10

    def test_special_geese_effects(self):
        # Prepare
        honk = HonkGoose("Noisy")
        unlucky = UnluckyGoose("Cursed")
        player = Mock()
        player.effects = Mock()

        # Action
        honk.attack_player(player)
        unlucky.attack_player(player)

        # Check
        player.effects.add.assert_any_call(
            "honk_damage", duration=3, power=honk.damage)
        player.effects.add.assert_any_call(
            "bad_luck", duration=5, power=unlucky.bad_luck_power)
        player.decrease_luck.assert_called_with(unlucky.bad_luck_power)

    def test_goose_group_management(self):
        # Prepare
        g1 = Goose("G1")
        g2 = Goose("G2")
        g2.health = 0
        group = GooseGroup([g1, g2])

        # Action
        alive_count = len(group.alive_geese)
        group.remove_dead_geese()

        # Check
        assert alive_count == 1
        assert len(group.geese) == 1
        assert "Group of 1 geese" in group.name

    def test_goose_group_metrics(self):
        # Prepare
        g1 = Goose("G1")
        g1.balance = 50
        g2 = Goose("G2")
        g2.balance = 100
        group = GooseGroup([g1, g2])

        # Action and Check
        assert group.total_balance == 150
        assert group.total_damage == 10
        assert group.steal_amount == 60

    def test_golden_goose_collection(self):
        # Prepare
        golden = GoldenGoose("Goldie")
        other_goose = Goose("Victim")
        other_goose.balance = 100
        player = Mock()

        # Action
        golden.attack_player(player, goose_collection=[golden, other_goose])

        # Check
        assert other_goose.balance == 50
        assert golden.balance == 25
        assert player.chips_income.called

    def test_unite_mechanics(self):
        # Prepare
        goose_a = Goose("A")
        goose_b = Goose("B")

        # Action
        new_group = goose_a + goose_b

        # Check
        assert isinstance(new_group, GooseGroup)
        assert len(new_group.geese) == 2

    def test_group_addition(self):
        # Prepare
        group = GooseGroup([Goose("A")])
        extra_goose = Goose("B")

        # Action
        new_group = group + extra_goose

        # Check
        assert len(group.geese) == 1
        assert len(new_group.geese) == 2
        assert new_group.geese[1].name == "B"

    def test_empty_group_repr(self):
        # Prepare
        group = GooseGroup([])

        # Action
        res = repr(group)

        # Check
        assert res == "GooseGroup[Empty]"

    def test_goose_group_attack_empty_or_dead(self):
        # Prepare
        dead_goose = Goose("Dead")
        dead_goose.health = 0
        group = GooseGroup([dead_goose])
        player = Mock()

        # Action
        damage, stolen = group.attack_player(player)

        # Check
        assert damage == 0
        assert group.name == "Empty group (all dead)"
        assert not group.is_alive

    def test_goose_steal_from_money_not_chips(self):
        # Prepare
        goose = Goose("Thief")
        player = Mock()
        player.name = "PoorInChips"
        player.get_chips_value.return_value = 0
        player.balance = 100

        # Action
        stolen = goose.steal_from_player(player)

        # Check
        assert stolen == 30
        player.balance_lesion.assert_called_with(30)

    def test_goose_steal_poor_player(self):
        # Prepare
        goose = Goose("Thief")
        player = Mock()
        player.get_chips_value.return_value = 0
        player.balance = 10

        # Action
        stolen = goose.steal_from_player(player)

        # Check
        assert stolen == 0

    def test_goose_attack_low_multiplier(self):
        # Prepare
        goose = Goose("Weak")
        player = Mock()

        # Action
        damage = goose.attack_player(player, damage_multiplier=0)

        # Check
        assert damage == goose.damage
        player.lose_health.assert_called_with(goose.damage)

    def test_war_goose_parry_branches(self):
        # Prepare
        warrior = WarGoose("Slayer")
        player = Mock()

        # Action
        with patch('src.infrastructure.goose.random', return_value=0.9):
            warrior.attack_player(player, damage_multiplier=4)

        # Check
        assert warrior.health < 15

    def test_golden_goose_collect_from_group_proportional(self):
        # Prepare
        golden = GoldenGoose("King")
        g1 = Goose("Rich")
        g1.balance = 80
        g2 = Goose("Poor")
        g2.balance = 20
        group = GooseGroup([g1, g2])
        player = Mock()

        # Action
        golden.attack_player(player, goose_collection=[group])

        # Check
        assert g1.balance == 40
        assert g2.balance == 10
        assert golden.balance == 25

    def test_golden_goose_collect_remaining_math(self):
        # Prepare
        golden = GoldenGoose("King")
        g1 = Goose("Target")
        g1.balance = 100
        group = GooseGroup([g1])

        # Action
        golden._collect_from_group(group, 50)

        # Check
        assert g1.balance == 50

    def test_goose_group_add_complex(self):
        # Prepare
        group_a = GooseGroup([Goose("A")])
        group_b = GooseGroup([Goose("B")])
        goose_c = Goose("C")

        # Action
        res1 = group_a + goose_c
        res2 = res1 + group_b

        # Check
        assert len(res1.geese) == 2
        assert len(res2.geese) == 3
        assert len(group_a.geese) == 1
        assert len(group_b.geese) == 1

    def test_goose_group_repr_alive_dead(self):
        # Prepare
        g1 = Goose("Alive")
        g2 = Goose("Dead")
        g2.health = 0
        group = GooseGroup([g1, g2])

        # Action
        res = repr(group)

        # Check
        assert "❤️Alive" in res
        assert "💀Dead" in res
        assert "🎯" in res

    def test_goose_group_steal_total(self):
        # Prepare
        g1 = Goose("A")
        g2 = Goose("B")
        group = GooseGroup([g1, g2])
        player = Mock()
        player.get_chips_value.return_value = 1000

        # Action
        total = group.steal_from_player(player)

        # Check
        assert total == 60

    def test_goose_attack_multiplier_branches(self):
        # Prepare
        goose = Goose("Tester")
        player = Mock()

        # Action and Check
        goose.attack_player(player, damage_multiplier=0)
        player.lose_health.assert_called_with(5)

        goose.attack_player(player, damage_multiplier=2)
        player.lose_health.assert_called_with(2)

    def test_goose_steal_skill_issue(self):
        # Prepare
        goose = Goose("Weakling")
        goose.steal_amount = 0
        player = Mock()
        # Action and Check
        assert goose.steal_from_player(player) == 0

    def test_war_goose_failed_hit(self):
        # Prepare
        war = WarGoose("Miser")
        player = Mock()
        # Action
        damage = war.attack_player(player, damage_multiplier=10)
        # Check
        assert damage == 0

    def test_goose_group_add_not_implemented(self):
        group = GooseGroup([])
        assert group.__add__(123) == NotImplemented

    def test_goose_unite_with_group(self):
        g1 = Goose("Solo")
        group = GooseGroup([Goose("Member")])
        new_group = g1 + group
        assert len(new_group.geese) == 2
        assert new_group.geese[-1] == g1

    def test_golden_goose_collect_logic_extended(self):
        golden = GoldenGoose("King")

        poor_goose = Goose("Poor")
        poor_goose.balance = 0
        golden.attack_player(Mock(), goose_collection=[poor_goose])
        assert golden.balance == 0

        empty_group = GooseGroup([])
        golden._collect_from_group(empty_group, 100)

        rich_goose = Goose("Rich")
        rich_goose.balance = 100
        group = GooseGroup([rich_goose])
        golden._collect_from_group(group, 50)
        assert rich_goose.balance == 50

    def test_goose_group_repr_complex(self):
        g1 = Goose("A")
        g2 = Goose("B")
        g2.health = 0
        group = GooseGroup([g1, g2])
        res = repr(group)
        assert "❤️A" in res
        assert "💀B" in res

    def test_war_goose_crit_and_parry(self):
        war = WarGoose("Elite")
        player = Mock()
        with patch('src.infrastructure.goose.random', return_value=0.0):
            damage = war.attack_player(player, damage_multiplier=1)
            assert damage == 20
