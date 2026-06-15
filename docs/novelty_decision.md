# Novelty Decision

## Chosen direction

Robotic plan recoverability: after an execution counterexample, the planner should evaluate a patched transition relation rather than only a globally updated prediction model.

## Final decision

Final v3 full-scale manuscript.

## Reasoning

- The paper no longer depends on a tiny exact-guard toy.
- Strong prediction-centric, uncertainty, blacklist, robust replanning, and oracle controls are included.
- The measured advantage is recoverability: repeated-counterexample reduction, stale-patch control, blocked-valid-transition accounting, and planner-cost tradeoffs.
- The full-scale suite covers domain families, counterexample families, planner families, repair mechanisms, guard policies, stresses, splits, seeds, horizons, patch budgets, alias levels, and rerolls.

## What we are not claiming

- Not a hardware-validated robot deployment.
- Not automatic guard learning.
- Not a universal planner.
- Not a replacement for learned world models.
- Not proof that every failure deserves a patch.

## Supported claim

In regimes where planners are likely to re-exploit sparse embodied counterexamples, counterexample-conditioned guarded transition repair is a useful planner-facing interface and should be evaluated with recoverability metrics beyond model loss and final success.
