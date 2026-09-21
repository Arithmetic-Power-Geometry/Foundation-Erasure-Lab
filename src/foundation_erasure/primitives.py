from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass


@dataclass(frozen=True)
class ToyFoundation:
    name: str
    secret: bytes

    def commit(self, semantic_state: str) -> str:
        return hashlib.sha256((self.name + "|" + semantic_state).encode()).hexdigest()

    def authenticate(self, message: str) -> str:
        return hmac.new(self.secret, message.encode(), hashlib.sha256).hexdigest()

    def verify(self, message: str, tag: str) -> bool:
        expected = self.authenticate(message)
        return hmac.compare_digest(expected, tag)


@dataclass
class CollapseOracle:
    foundation: ToyFoundation

    def forge(self, message: str) -> str:
        return self.foundation.authenticate(message)

    def arbitrary_old_commit(self, semantic_state: str) -> str:
        return self.foundation.commit(semantic_state)
