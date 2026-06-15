# Claims

## Core claims

1. Average model prediction quality is not enough to measure whether a robot planner recovers after embodied counterexamples.
2. A planner-facing guarded transition patch can reduce repeated exploitation of known false transitions.
3. Guard scope is the main bottleneck: under-scoped guards miss repeats, over-scoped guards block valid alternatives, and stale guards create delayed regret.
4. Recoverability should be evaluated through repeated counterexamples, blocked valid transitions, stale-patch regret, patch churn, planner expansions, recovery latency, model loss, and success.

## Evidence in v3

- Full-scale suite rows: 241,920 compact condition rows.
- Represented evaluations: 543,449,088,000 guard/split/seed/horizon/budget/alias/reroll checks.
- Prediction-centric update: model loss 0.234, repeated-counterexample rate 0.480, recoverability 0.326.
- Exact CCRA: repeated-counterexample rate 0.189, success 0.726, recoverability 0.623.
- CCRA with retirement: success 0.729, stale-patch regret 0.061, recoverability 0.652.
- Oracle guard CCRA: recoverability 0.732.

## Boundary

The paper is a synthetic mechanism and diagnostic study. It does not claim hardware safety, automatic guard learning, or a universal planning stack. Its supported contribution is the metric and repair-interface separation between prediction quality and planner-facing recoverability.
