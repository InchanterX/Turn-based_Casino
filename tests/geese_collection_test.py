from src.infrastructure.collections.geese import GooseCollection


def test_goose_collection_basic_operations():
    # Prepare
    g = GooseCollection()
    g.append("G1")
    g.append("G2")

    # Action and Check
    assert len(g) == 2
    assert g[0] == "G1"
    assert g[1] == "G2"
    assert list(iter(g)) == ["G1", "G2"]

    s = g[0:1]
    assert isinstance(s, GooseCollection)
    assert len(s) == 1
    assert s[0] == "G1"

    # remove
    g.remove("G1")
    assert len(g) == 1
    assert g[0] == "G2"
