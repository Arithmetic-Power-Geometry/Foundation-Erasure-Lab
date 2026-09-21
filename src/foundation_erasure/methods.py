from __future__ import annotations

from dataclasses import dataclass
from .finality import FinalityRegistry
from .model import CanonicalState, SecurityDependencyGraph
from .primitives import ToyFoundation

@dataclass
class MigrationResult:
    method: str
    old_root: str
    new_root: str
    canonical_root: str
    graph: SecurityDependencyGraph

def _result(method, state, old, new, finality, graph, new_root):
    finality.finalize(state.identity, new_root)
    return MigrationResult(method, old.commit(state.canonical()), new_root, new_root, graph)

def key_rotation_same_foundation(state, old, new, finality):
    g=SecurityDependencyGraph()
    g.add(old.name,"current_state"); g.add(new.name,"current_state"); g.add("finality","current_state")
    return _result("key_rotation",state,old,new,finality,g,new.commit(state.canonical()))

def wrapped_old_root(state, old, new, finality):
    old_root=old.commit(state.canonical()); g=SecurityDependencyGraph()
    g.add(old.name,"old_root"); g.add("old_root","current_state"); g.add(new.name,"current_state"); g.add("finality","current_state")
    return _result("wrapped_old_root",state,old,new,finality,g,new.commit(old_root))

def chained_successor_authorization(state, old, new, finality):
    old_root=old.commit(state.canonical()); _=old.authenticate(f"{state.identity}|{old_root}|{new.name}")
    g=SecurityDependencyGraph()
    g.add(old.name,"transition_authority"); g.add("transition_authority","current_state"); g.add(new.name,"current_state"); g.add("finality","current_state")
    return _result("chained_successor",state,old,new,finality,g,new.commit(state.canonical()))

def evidence_renewal_chain(state, old, new, finality):
    """ERS-like abstract baseline: current evidence preserves an authenticated chain to prior evidence."""
    old_root=old.commit(state.canonical()); renewed=new.commit(old_root+"|evidence")
    g=SecurityDependencyGraph()
    g.add(old.name,"archival_evidence"); g.add("archival_evidence","current_state"); g.add(new.name,"current_state"); g.add("finality","current_state")
    return _result("evidence_renewal",state,old,new,finality,g,renewed)

def dual_hybrid_anchor(state, old, new, finality):
    """Hybrid transition retaining both old and new foundations as active dependencies."""
    new_root=new.commit(state.canonical()); g=SecurityDependencyGraph()
    g.add(old.name,"current_state"); g.add(new.name,"current_state"); g.add("finality","current_state")
    return _result("dual_hybrid_anchor",state,old,new,finality,g,new_root)

def proactive_refresh(state, old, new, finality):
    """Abstract proactive/key-refresh baseline: refreshes key material but retains family-level dependency."""
    new_root=new.commit(state.canonical()); g=SecurityDependencyGraph()
    g.add(old.name,"family_assumption"); g.add("family_assumption","current_state"); g.add(new.name,"current_state"); g.add("finality","current_state")
    return _result("proactive_refresh",state,old,new,finality,g,new_root)

def transparency_rollover(state, old, new, finality):
    """Abstract transparency/key-rollover baseline: history authenticates successor while log prevents equivocation."""
    new_root=new.commit(state.canonical()); g=SecurityDependencyGraph()
    g.add(old.name,"rollover_history"); g.add("rollover_history","current_state"); g.add(new.name,"current_state"); g.add("finality","current_state")
    return _result("transparency_rollover",state,old,new,finality,g,new_root)

def semantic_reanchor(state, old, new, finality):
    old_root=old.commit(state.canonical()); new_root=new.commit(state.canonical())
    g=SecurityDependencyGraph()
    g.add(new.name,"current_state"); g.add("finality","current_state")
    return MigrationResult("semantic_reanchor",old_root,new_root,new_root,g)
