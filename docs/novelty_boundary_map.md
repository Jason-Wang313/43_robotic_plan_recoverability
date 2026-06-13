# Novelty Boundary Map

## Not enough on its own

- Bigger model.
- Better data.
- New benchmark only.
- Add uncertainty.
- Add active learning.
- Add verifier.
- Combine two existing modules.
- Use an LLM as planner.
- Use reinforcement learning.

## Stronger boundary

The strongest shape is a deployment-time repair operator: after an embodied counterexample, the system updates the planner-facing transition model, not just a score, detector, or retraining set.

## Hidden assumptions broken

- Prediction loss is enough for control.
- Repairs should be global.
- Replanning after failure is sufficient.
- Uncertainty is the right trigger.
- A detached verifier is enough.
- One-step accuracy is the objective.
- Failures are independent.
- Small smooth updates are always better.

## V2 boundary update

The mechanism is only defensible under calibrated guard scope. Exact guards produce the clean no-repeat behavior, under-scoped guards miss repeated false shortcuts, and over-scoped guards block valid shortcuts and increase search.
