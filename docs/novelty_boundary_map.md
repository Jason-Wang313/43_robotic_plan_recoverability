# Novelty Boundary Map

## Not Enough On Its Own
- bigger model
- better data
- new benchmark only
- add uncertainty
- add active learning
- add verifier
- combine two existing modules
- use an LLM as planner
- use reinforcement learning

## Stronger Boundary
The strongest shape is a deployment-time repair operator: after an embodied counterexample, the system updates the planner-facing transition model, not just a score, detector, or retraining set.

## Hidden Assumptions Broken
1. Prediction loss is enough for control. Because Sparse planner-exploited errors can dominate success. Direction: Center repair on the counterexample that actually hurts planning.
2. Repairs should be global. Because Many mismatch modes are local and structural. Direction: Use guarded local transition edits.
3. Replanning after failure is sufficient. Because The same false transition can be exploited again. Direction: Make the model itself remember the counterexample.
4. Uncertainty is the right trigger. Because Confident wrong models can still be exploited. Direction: Trigger repair from execution contradictions.
5. Residuals are smooth. Because Contact and affordance changes can be discontinuous. Direction: Allow guarded discontinuous patches.
6. Domain randomization covers deployment. Because Deployment may introduce unseen contact regimes. Direction: Repair at deployment time.
7. A verifier is enough. Because A detached check does not change future rollouts. Direction: Update the planner-facing model.
8. Reward reveals the failure. Because A failed transition is visible before reward accumulates. Direction: Use action-outcome contradictions.
9. A learned latent preserves the repair variable. Because Latents may hide the causal variable. Direction: Keep repairs anchored to observable predicates when possible.
10. Environment stationarity is a safe assumption. Because Robots change the world as they act. Direction: Give patches explicit scope and retirement conditions.
11. Planner errors are downstream only. Because Planners actively exploit optimistic false transitions. Direction: Use planner-exploitation counterexamples.
12. One-step accuracy is the objective. Because Long-horizon plan validity is the objective. Direction: Evaluate repeated-failure prevention.
13. More data is always enough. Because A structural omission may need a transition edit. Direction: Separate data collection from model repair.
14. Recovery is mainly a policy problem. Because Sometimes the world model is the bottleneck. Direction: Repair before replanning.
15. Confidence routing solves action choice. Because It does not rewrite the false transition. Direction: Make repair central.
16. A single training objective fits all users. Because Prediction and planning value different errors. Direction: Use a control-weighted repair objective.
17. Failures are independent. Because The same hole can be exploited repeatedly. Direction: Track exact repeated exploitation.
18. Semantic priors dominate physical evidence. Because Grounded counterexamples should override them. Direction: Let execution win over priors.
19. Benchmark success generalizes to the tail. Because Rare critical errors can be hidden by averages. Direction: Stress sparse critical mismatches.
20. Small updates are always better. Because Some changes are discontinuous. Direction: Permit minimal discontinuous edits.
21. The right abstraction is fixed. Because A failure may reveal a missing state distinction. Direction: Allow repairs to create new guards.
