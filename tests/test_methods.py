from foundation_erasure.finality import FinalityRegistry
from foundation_erasure.methods import semantic_reanchor, wrapped_old_root
from foundation_erasure.metrics import measure
from foundation_erasure.model import CanonicalState
from foundation_erasure.primitives import ToyFoundation


def test_semantic_reanchor_erases_old_dependency():
    state = CanonicalState("i", 1, "a", "p")
    old = ToyFoundation("old", b"a")
    new = ToyFoundation("new", b"b")
    r = semantic_reanchor(state, old, new, FinalityRegistry())
    m = measure(r, "old", "new")
    assert m.old_foundation_active == 0
    assert m.retirement_debt == 0


def test_wrapped_root_keeps_old_dependency():
    state = CanonicalState("i", 1, "a", "p")
    old = ToyFoundation("old", b"a")
    new = ToyFoundation("new", b"b")
    r = wrapped_old_root(state, old, new, FinalityRegistry())
    m = measure(r, "old", "new")
    assert m.old_foundation_active == 1
    assert m.retirement_debt == 1
