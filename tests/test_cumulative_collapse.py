from foundation_erasure.experiments.cumulative_collapse import build,attack,ATTACKS

def test_all_128_retired_epochs_cannot_replace_current_state():
    T=128
    for i in range(T):
        for a in ATTACKS:
            j,h=build(T)
            assert attack(j,h,i,a)==0
