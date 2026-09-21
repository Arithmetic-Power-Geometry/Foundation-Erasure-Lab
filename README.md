# Foundation Erasure Lab

Reproducible research software for cryptographic retirement, semantic re-anchoring with atomic finality, retired-foundation collapse, and telescoping security.

## Research objective

A cryptographic migration is considered fully retired for current-state security only when compromise of a retired foundation no longer increases an adversary's ability to alter the current accepted canonical state.

This repository implements and evaluates the following core concepts:

- **Active Security Frontier (ASF)**: security resources whose compromise can increase an adversary's ability to replace the current canonical state.
- **Retirement Debt (RD)**: retired foundations that remain in the current active security frontier.
- **Foundation Erasure (FE)**: a retired foundation is absent from the current active security frontier.
- **Semantic Re-Anchoring with Atomic Finality**: the successor independently authenticates the complete decision-relevant state; finalization establishes the successor as the unique current authority and removes retired authority from current-state verification.
- **Post-Finalization Collapse Non-Interference (PFCNI)**: collapse of a retired foundation after finalization does not increase the adversary's current-state replacement capability.
- **Retirement Point**: the transition point after which retired authority no longer has current write authority in the implemented state machine.
- **Telescoping Security**: cryptographic history can grow while current-state security dependence remains bounded by active resources rather than accumulating across retired foundations.

## Experimental workflow

1. Implement structural migration comparators and semantic re-anchoring.
2. Exercise migration, authorization, and atomic finalization.
3. Execute retired-key, retired-family, rollback, replay, fork, substitution, reordering, omission, and cumulative-collapse scenarios.
4. Measure attack acceptance, retirement debt, active-security-frontier size, verifier dependencies, and primitive-level performance.
5. Produce machine-readable CSV and JSON result artifacts.
6. Reproduce the complete experimental suite through GitHub Actions.

## Comparators

The comparative benchmark uses structural migration patterns rather than claiming full protocol implementations:

- key rotation without foundation change
- old-root wrapping under a new foundation
- chained successor authorization
- evidence-renewal-like dependency retention
- dual/hybrid anchoring
- proactive/key-refresh-like dependency retention
- transparency-rollover-like dependency retention
- semantic re-anchoring with atomic finality

Standards and mechanisms such as evidence renewal and trust-anchor rollover are prior-art neighbors, not faithfully implemented protocol baselines in this repository.

## Adversarial scenarios

- retired-key compromise
- modeled retired-family collapse
- rollback
- successor substitution
- replay
- fork / split-history attempt
- history reordering
- epoch omission
- cumulative compromise across retired epochs

The collapse experiments evaluate whether compromised retired authority can change the current canonical state. They do **not** constitute cryptanalytic breaks of RSA, ECDSA, or ML-DSA.

## Reproducibility

Install the package and run:

```bash
python -m foundation_erasure.experiments.run_all --out results
```

The GitHub Actions workflow runs the test suite and experimental protocols and uploads the generated `results/` directory as a workflow artifact.

The experimental suite includes real RSA-2048, ECDSA P-256, and ML-DSA-44 signing/verification measurements; active-security-frontier and retirement-debt experiments; verifier dependency traces; retirement-point analysis; cross-family post-finalization state-replacement attempts; and cumulative-collapse evaluation through 128 epochs.

The protocol-state experiments model compromise as adversarial control of retired authority and test whether that authority can modify the currently accepted canonical state. Primitive benchmarks and protocol-state security experiments are therefore reported as distinct evidence layers.

## Scope

The software evaluates current-state cryptographic retirement. Historical provenance is a separate security objective and may continue to require archival evidence, timestamps, transparency mechanisms, certificates, or other historical verification resources.

The current foundation and active finality mechanism remain security-critical resources. Foundation Erasure removes retired foundations from current-state security dependence; it does not eliminate all cryptographic trust.

## Citation

If you use this software or the Foundation Erasure framework, cite:

Akhtar, M. A. K. (2026). *Foundation Erasure: Bounded Cryptographic Dependence After Repeated Algorithm Migration* (Version V1). Zenodo. https://doi.org/10.5281/zenodo.22878898

```bibtex
@misc{Akhtar2026FoundationErasure,
  author    = {Akhtar, Mohammad Amir Khusru},
  title     = {Foundation Erasure: Bounded Cryptographic Dependence After Repeated Algorithm Migration},
  year      = {2026},
  version   = {V1},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.22878898},
  url       = {https://doi.org/10.5281/zenodo.22878898}
}
```

## Status

Research software under active development. Results are produced by executable experiments and reproducible workflows.
