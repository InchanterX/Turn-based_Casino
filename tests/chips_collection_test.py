from src.infrastructure.collections.chips import Chip, ChipsCollection
import pytest


def test_chip_invalid_denomination_raises():
    with pytest.raises(ValueError):
        Chip(3, 1)


def test_chip_add_and_sub():
    # Prepare
    a = Chip(5, 2)
    b = Chip(5, 3)

    # Action
    c = a + b
    assert c.denomination == 5
    assert c.quantity == 5

    d = a - Chip(5, 5)
    assert d.denomination == 5
    assert d.quantity == 0


def test_chips_collection_init_and_total_and_info_repr():
    # Prepare and Action
    col = ChipsCollection(131)

    # Check
    assert col.total_value() == 131
    assert col.get_info() == "100:1, 25:1, 5:1, 1:1"
    assert repr(col) == "Chips: 100:1, 25:1, 5:1, 1:1"


def test_add_and_remove_behavior():
    # Prepare
    c = ChipsCollection()
    c.add(37)

    # Check
    assert c.total_value() == 37

    assert c.remove(20) is True
    assert c.total_value() == 17

    assert c.remove(1000) is False
    assert c.total_value() == 17


def test_remove_exact_total_sets_zero():
    # Prepare
    c = ChipsCollection(100)

    # Action
    assert c.total_value() == 100
    assert c.remove(100) is True
    assert c.total_value() == 0
    assert c.get_info() == "no chips"
