from unittest.mock import Mock
from src.infrastructure.collections.geese import GooseCollection


def test_goose_collection_basic_operations():
    # Prepare
    g = GooseCollection()

    goose1 = Mock()
    goose1.name = "G1"

    goose2 = Mock()
    goose2.name = "G2"

    g.append(goose1)
    g.append(goose2)

    assert len(g) == 2
    assert g[0] == goose1
    assert g[1] == goose2

    names = [goose.name for goose in g]
    assert names == ["G1", "G2"]

    g.remove(goose1)
    assert len(g) == 1
    assert g[0] == goose2
