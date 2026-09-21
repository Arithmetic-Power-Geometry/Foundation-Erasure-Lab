from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class FinalityRegistry:
    """Minimal non-equivocating canonical-root registry used as an active resource."""

    current: Dict[str, str] = field(default_factory=dict)

    def finalize(self, identity: str, root: str) -> None:
        self.current[identity] = root

    def canonical(self, identity: str) -> str | None:
        return self.current.get(identity)
