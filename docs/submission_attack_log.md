# Submission Attack Log

## Attack: exact guard dependence

Question: Does the result depend on perfectly scoped guards?

Result: the v2 stress showed that guard scope is a central assumption. The v3 suite includes eight guard policies and reports precision, recall, blocked valid transitions, repeated counterexamples, and stale-patch regret.

Decision impact: final paper makes guard scope a measured bottleneck.

## Attack: prediction-centric update is enough

Question: Can model update solve the problem without planner-facing patches?

Result: prediction-centric update has low model loss but repeated-counterexample rate 0.480 and recoverability 0.326, below exact CCRA and CCRA with retirement.

Decision impact: supports the metric separation between prediction quality and recoverability.

## Attack: robust replanning is enough

Question: Can conservative replanning solve the problem by expanding more alternatives?

Result: robust replanning has higher mean expansions and lower recoverability than CCRA variants in the full-scale suite.

Decision impact: supports the need for transition-level repair objects.

## Attack: real-robot readiness

Question: Is there hardware or high-fidelity contact evidence?

Result: no. The paper is framed as a full-scale synthetic mechanism study with hardware validation plans and falsification criteria.

Decision impact: limits the claim to representation, metrics, and diagnostics.
