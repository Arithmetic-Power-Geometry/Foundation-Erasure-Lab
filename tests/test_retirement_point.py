from foundation_erasure.experiments.retirement_point import trial,ATTACKS
from foundation_erasure.state_machine import Phase

def test_collapse_before_finality_is_not_claimed_safe():
    for p in (Phase.OLD,Phase.PREPARED,Phase.AUTHORIZED):
        assert all(trial(p,a)==1 for a in ATTACKS)

def test_retired_family_cannot_change_finalized_state():
    assert all(trial(Phase.FINALIZED,a)==0 for a in ATTACKS)
