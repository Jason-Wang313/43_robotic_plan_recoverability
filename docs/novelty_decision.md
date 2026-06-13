# Novelty Decision

Chosen thesis: embodied plan recoverability should be measured and improved by how execution counterexamples rewrite the transition relation used by planning.

Chosen mechanism: Counterexample-Conditioned Repair Automata (CCRA).

Decision after v2 hardening: workshop-only.

Reasoning:
- The hostile set already covers prediction, MPC, adaptation, uncertainty, and recovery.
- The less occupied boundary is an immediate planner-facing repair loop.
- The v2 stress confirms that the mechanism depends on calibrated guard scope.
- Under-scoped guards miss failures, and over-scoped guards raise search cost.
- No real-robot, perception, or automatic guard-learning evidence is present.

Minimal surviving claim: CCRA is a useful mechanism probe for planner-facing recoverability when guards are sufficiently calibrated.
