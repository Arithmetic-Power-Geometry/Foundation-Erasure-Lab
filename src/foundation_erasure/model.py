from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Set


@dataclass
class CanonicalState:
    identity: str
    epoch: int
    authority: str
    payload: str

    def canonical(self) -> str:
        return f"{self.identity}|{self.epoch}|{self.authority}|{self.payload}"


@dataclass
class SecurityDependencyGraph:
    edges: Dict[str, Set[str]] = field(default_factory=dict)

    def add(self, source: str, target: str) -> None:
        self.edges.setdefault(source, set()).add(target)

    def reachable(self, source: str, target: str) -> bool:
        seen = set()
        stack = [source]
        while stack:
            node = stack.pop()
            if node == target:
                return True
            if node in seen:
                continue
            seen.add(node)
            stack.extend(self.edges.get(node, ()))
        return False

    def active_security_frontier(self, current_state_node: str, resources: Iterable[str]) -> Set[str]:
        return {r for r in resources if self.reachable(r, current_state_node)}

    def retirement_debt(self, current_state_node: str, retired_foundations: Iterable[str]) -> Set[str]:
        return {f for f in retired_foundations if self.reachable(f, current_state_node)}
