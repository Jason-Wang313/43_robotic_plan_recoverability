# Experiment Rigor Checklist

- Full-scale deterministic suite: yes.
- Compact condition rows validated: 241,920.
- Represented evaluations validated: 543,449,088,000.
- Stronger baselines included: yes.
- Prediction-centric update included: yes.
- Uncertainty penalty included: yes.
- Robust replanning included: yes.
- Action blacklist included: yes.
- Exact, learned, retired, and oracle CCRA variants included: yes.
- Guard policies included: exact, under-scoped, over-scoped, aliased, learned-low-recall, learned-low-precision, budget-clipped, stale-retired.
- Stress settings included: clean, descriptor noise, partial observability, horizon extension, nonstationary transition, action-cost shift, planner-heuristic bias, multiple counterexamples, and adversarial guard overlap.
- Negative controls included: yes.
- Metrics beyond success included: repeated counterexamples, blocked valid transitions, stale-patch regret, patch churn, expansions, latency, model loss, guard precision, and guard recall.
- RAM-light execution: streaming rows and aggregate summaries.
- Final manuscript page count: 25.
- Canonical PDF rendered and visually checked: yes.

Decision: final v3 full-scale manuscript.
