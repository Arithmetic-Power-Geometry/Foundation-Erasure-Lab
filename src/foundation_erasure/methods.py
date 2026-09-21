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


def key_rotation_same_foundation(
    state: CanonicalState,
    old: ToyFoundation,
    new_key_same_family: ToyFoundation,
    finality: FinalityRegistry,
) -> MigrationResult:
    old_root = old.commit(state.canonical())
    new_root = new_key_same_family.commit(state.canonical())
    finality.finalize(state.identity, new_root)
    g = SecurityDependencyGraph()
    g.add(old.name, "current_state")
    g.add(new_key_same_family.name, "current_state")
    g.add("finality", "current_state")
    return MigrationResult("key_rotation", old_root, new_root, new_root, g)


def wrapped_old_root(
    state: CanonicalState,
    old: ToyFoundation,
    new: ToyFoundation,
    finality: FinalityRegistry,
) -> MigrationResult:
    old_root = old.commit(state.canonical())
    # Baseline: successor binds only the old digest, preserving dependence on old binding.
    new_root = new.commit(old_root)
    finality.finalize(state.identity, new_root)
    g = SecurityDependencyGraph()
    g.add(old.name, "old_root")
    g.add("old_root", "current_state")
    g.add(new.name, "current_state")
    g.add("finality", "current_state")
    return MigrationResult("wrapped_old_root", old_root, new_root, new_root, g)


def chained_successor_authorization(
    state: CanonicalState,
    old: ToyFoundation,
    new: ToyFoundation,
    finality: FinalityRegistry,
) -> MigrationResult:
    old_root = old.commit(state.canonical())
    transition = f"{state.identity}|{old_root}|{new.name}"
    _old_authorization = old.authenticate(transition)
    new_root = new.commit(state.canonical())
    finality.finalize(state.identity, new_root)
    g = SecurityDependencyGraph()
    g.add(old.name, "transition_authority")
    g.add("transition_authority", "current_state")
    g.add(new.name, "current_state")
    g.add("finality", "current_state")
    return MigrationResult("chained_successor", old_root, new_root, new_root, g)


def semantic_reanchor(
    state: CanonicalState,
    old: ToyFoundation,
    new: ToyFoundation,
    finality: FinalityRegistry,
) -> MigrationResult:
    old_root = old.commit(state.canonical())
    # Proposed method: independently bind the full semantic state under successor foundation.
    new_root = new.commit(state.canonical())
    finality.finalize(state.identity, new_root)
    g = SecurityDependencyGraph()
    g.add(new.name, "current_state")
    g.add("finality", "current_state")
    return MigrationResult("semantic_reanchor", old_root, new_root, new_root, g)
