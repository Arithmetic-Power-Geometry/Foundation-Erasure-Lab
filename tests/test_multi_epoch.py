from foundation_erasure.experiments.multi_epoch import chain_graph

def test_telescoping_retirement_does_not_accumulate_old_foundations():
    for t in (2,4,8,16):
        g=chain_graph("semantic_reanchor",t)
        assert all(not g.reachable(f"F{i}","current_state") for i in range(t))
        assert g.reachable(f"F{t}","current_state")

def test_wrapped_chain_accumulates_retirement_debt():
    g=chain_graph("wrapped_chain",8)
    assert sum(g.reachable(f"F{i}","current_state") for i in range(8))==8
