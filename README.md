# Foundation Erasure Lab

Software-first reproducible experiments for cryptographic retirement, semantic re-anchoring, retired-foundation collapse, and telescoping security.

## Research objective

A cryptographic migration is considered complete only when compromise of a retired foundation no longer increases the adversary's ability to alter the current trusted state.

This repository develops and tests four core ideas:

- **Active Security Frontier (ASF)**: the resources whose compromise can currently affect accepted canonical state.
- **Foundation Erasure (FE)**: a retired foundation is absent from the current ASF.
- **Semantic Re-Anchoring (SRA)**: the successor foundation independently binds the canonical semantic state instead of merely wrapping an old digest.
- **Telescoping Security (TS)**: after finalized handoff, retired foundations disappear from the current security dependency set.

## Software-first workflow

1. Implement baseline migration strategies.
2. Implement semantic re-anchoring.
3. Execute retired-key and retired-family collapse attacks.
4. Measure attack success, retirement debt, active-security-frontier size, and runtime overhead.
5. Generate CSV/JSON artifacts through GitHub Actions.
6. Compare methods from generated artifacts.
7. Write the manuscript only after the empirical separation is stable and reproducible.

## Baselines

The comparative benchmark uses structural migration patterns rather than claiming full protocol implementations:

- key rotation without foundation change
- old-root wrapping under a new foundation
- chained successor authorization
- evidence-renewal-like dependency retention
- dual/hybrid anchoring
- proactive/key-refresh-like dependency retention
- transparency-rollover-like dependency retention
- semantic re-anchoring

Standards such as ERS and trust-anchor rollover are treated as prior-art neighbors, not as faithfully implemented benchmark protocols.

## Attacks

- retired-key compromise
- modeled retired-family collapse
- rollback
- successor substitution
- replay
- fork / split-history attempt
- history reordering and epoch omission
- cumulative compromise across all retired epochs

The collapse experiments evaluate whether compromised retired authority can change the current canonical state. They do not constitute cryptanalytic breaks of RSA, ECDSA, or ML-DSA.

## Reproducibility

Run:

```bash
python -m foundation_erasure.experiments.run_all --out results
```

The GitHub Actions workflow runs tests, reproduces the benchmark suite, and uploads the generated `results/` directory as a workflow artifact.

## Reproducible evidence

The workflow also benchmarks real RSA-2048, ECDSA P-256, and ML-DSA-44 signing/verification primitives, traces the security resources consulted by the current-state verifier, tests the handoff retirement point, and exercises cumulative post-finalization attacks through 128 epochs.

## Status

Research software under active development. Results are generated from executable code and workflow artifacts; no manuscript values are hard-coded.
