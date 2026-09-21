from __future__ import annotations

from dataclasses import dataclass

from .methods import MigrationResult


@dataclass
class Metrics:
    method: str
    old_foundation_active: int
    active_security_frontier_size: int
    retirement_debt: int


def measure(result: MigrationResult, old_name: str, new_name: str) -> Metrics:
    resources = {old_name, new_name, "finality"}
    asf = result.graph.active_security_frontier("current_state", resources)
    debt = result.graph.retirement_debt("current_state", [old_name])
    return Metrics(
        method=result.method,
        old_foundation_active=int(old_name in asf),
        active_security_frontier_size=len(asf),
        retirement_debt=len(debt),
    )
