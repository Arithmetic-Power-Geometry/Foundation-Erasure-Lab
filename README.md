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

- key rotation without foundation change
- old-root wrapping under a new foundation
- chained successor authorization
- semantic re-anchoring

## Attacks

- retired-key compromise
- retired-family collapse
- rollback
- successor substitution
- fork / split-history attempt

## Reproducibility

Run:

```bash
python -m foundation_erasure.experiments.run_all --out results
```

The GitHub Actions workflow runs tests, reproduces the benchmark suite, and uploads the generated `results/` directory as a workflow artifact.

## Status

Research software under active development. Results are generated from code; no manuscript numbers are hard-coded.
