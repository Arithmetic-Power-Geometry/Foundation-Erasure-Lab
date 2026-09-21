from __future__ import annotations

from dataclasses import dataclass

from .finality import FinalityRegistry
from .model import CanonicalState
from .methods import MigrationResult
from .primitives import CollapseOracle, ToyFoundation


@dataclass
class AttackOutcome:
    attack: str
    success: bool


def retired_family_collapse(
    legitimate: CanonicalState,
    forged: CanonicalState,
    result: MigrationResult,
    old: ToyFoundation,
    new: ToyFoundation,
    finality: FinalityRegistry,
) -> AttackOutcome:
    oracle = CollapseOracle(old)
    _ = oracle.forge(f"successor:{forged.canonical()}")
    _ = oracle.arbitrary_old_commit(forged.canonical())

    # If old foundation still reaches current_state in the dependency graph,
    # collapse is counted as security-relevant and the attack succeeds in this abstract model.
    success = result.graph.reachable(old.name, "current_state")
    return AttackOutcome("retired_family_collapse", success)


def rollback_attack(result: MigrationResult, old: ToyFoundation) -> AttackOutcome:
    return AttackOutcome("rollback", result.graph.reachable(old.name, "current_state"))


def successor_substitution(result: MigrationResult, old: ToyFoundation) -> AttackOutcome:
    return AttackOutcome("successor_substitution", result.graph.reachable(old.name, "current_state"))


def fork_attack(result: MigrationResult, old: ToyFoundation) -> AttackOutcome:
    return AttackOutcome("fork", result.graph.reachable(old.name, "current_state"))
