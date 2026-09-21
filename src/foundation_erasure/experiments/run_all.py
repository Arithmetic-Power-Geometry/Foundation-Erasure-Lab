from __future__ import annotations

import argparse
import csv
import json
import time
from pathlib import Path

from foundation_erasure.attacks import (
    fork_attack,
    retired_family_collapse,
    rollback_attack,
    successor_substitution,
)
from foundation_erasure.finality import FinalityRegistry
from foundation_erasure.methods import (
    chained_successor_authorization,
    key_rotation_same_foundation,
    semantic_reanchor,
    wrapped_old_root,
)
from foundation_erasure.metrics import measure
from foundation_erasure.model import CanonicalState
from foundation_erasure.primitives import ToyFoundation


def run(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)

    legitimate = CanonicalState("identity-001", 1, "owner-A", "canonical-payload")
    forged = CanonicalState("identity-001", 1, "attacker-X", "forged-payload")
    old = ToyFoundation("legacy-family-A", b"legacy-secret")
    rotated = ToyFoundation("legacy-family-A-rotated", b"rotated-secret")
    successor = ToyFoundation("successor-family-B", b"successor-secret")

    methods = [
        ("key_rotation", lambda f: key_rotation_same_foundation(legitimate, old, rotated, f), rotated),
        ("wrapped_old_root", lambda f: wrapped_old_root(legitimate, old, successor, f), successor),
        ("chained_successor", lambda f: chained_successor_authorization(legitimate, old, successor, f), successor),
        ("semantic_reanchor", lambda f: semantic_reanchor(legitimate, old, successor, f), successor),
    ]

    metric_rows = []
    attack_rows = []
    timing_rows = []

    for _, builder, current in methods:
        finality = FinalityRegistry()
        t0 = time.perf_counter_ns()
        result = builder(finality)
        elapsed = time.perf_counter_ns() - t0

        m = measure(result, old.name, current.name)
        metric_rows.append(vars(m))
        timing_rows.append({"method": result.method, "handoff_ns": elapsed})

        attacks = [
            retired_family_collapse(legitimate, forged, result, old, current, finality),
            rollback_attack(result, old),
            successor_substitution(result, old),
            fork_attack(result, old),
        ]
        for a in attacks:
            attack_rows.append({"method": result.method, "attack": a.attack, "success": int(a.success)})

    with (out / "foundation_erasure.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=metric_rows[0].keys())
        w.writeheader()
        w.writerows(metric_rows)

    with (out / "attack_success.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=attack_rows[0].keys())
        w.writeheader()
        w.writerows(attack_rows)

    with (out / "performance.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=timing_rows[0].keys())
        w.writeheader()
        w.writerows(timing_rows)

    manifest = {
        "schema": 1,
        "methods": [x[0] for x in methods],
        "attacks": sorted({r["attack"] for r in attack_rows}),
        "note": "Synthetic abstract security-dependency experiment; not a claim of real-world cryptanalytic break rates.",
    }
    (out / "experiment_manifest.json").write_text(json.dumps(manifest, indent=2))

    dependency_frontier = {
        row["method"]: {
            "old_foundation_active": row["old_foundation_active"],
            "active_security_frontier_size": row["active_security_frontier_size"],
            "retirement_debt": row["retirement_debt"],
        }
        for row in metric_rows
    }
    (out / "dependency_frontier.json").write_text(json.dumps(dependency_frontier, indent=2))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="results")
    args = p.parse_args()
    run(Path(args.out))


if __name__ == "__main__":
    main()
