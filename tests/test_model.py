from foundation_erasure.model import SecurityDependencyGraph


def test_reachability_and_retirement_debt():
    g = SecurityDependencyGraph()
    g.add("old", "transition")
    g.add("transition", "current")
    assert g.reachable("old", "current")
    assert g.retirement_debt("current", ["old"]) == {"old"}
