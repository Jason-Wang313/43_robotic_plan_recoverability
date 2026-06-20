# Paper 43 Full-Scale Execution Plan

Paper: `43_robotic_plan_recoverability`

Working title: `Robotic Plan Recoverability: Counterexample-Conditioned Repair Automata Under Guard Scope, Staleness, and Planner Cost`

Date: 2026-06-15

## Starting State

The repository contains a short v2 narrowing note. The prior guard-scope stress is useful and must be preserved as a baseline lesson: exact CCRA reaches 1.000 success, under-scoped guards fall to 0.859 success, and over-scoped guards keep success only by increasing mean expansions from 2.008 to 2.746. The final paper must therefore avoid claiming that planner-facing repair is solved. The recoverable contribution is narrower and stronger: plan recoverability should be evaluated as its own objective, with guard scope, repeated counterexamples, false-positive blocking, stale patches, and search cost measured directly.

There is no current `C:/Users/wangz/Downloads/43.pdf` artifact. The old canonical size recorded in docs is stale.

## Current Claim

Full-scale claim to test:

1. Average model prediction quality is not enough to measure whether a robot planner recovers after embodied counterexamples.
2. Counterexample-conditioned repair can prevent repeated exploitation of false transitions when the repair is represented as a planner-facing guarded patch.
3. Guard scope is the main bottleneck: under-scoped patches miss repeated failures, over-scoped patches block valid plans, and stale patches can create delayed regret.
4. The right evaluation unit is not only episode success. It is recoverability: repeated counterexample rate, time-to-recovery, guard precision/recall, blocked-valid-transition rate, patch churn, stale-patch regret, and planner expansion cost.

## Gaps To Close

- Current evidence is a small simulation with one false-shortcut mechanism.
- Current stress evaluates guard scope but not guard precision/recall, stale patch retirement, patch budgets, horizon length, planner type, aliasing, nonstationarity, or multi-counterexample interaction.
- There is no broad comparison against prediction-centric replanning, uncertainty avoidance, global retraining, action blacklisting, robust planning, or patch retirement.
- There are no domain families, failure families, planner families, stress regimes, patch-budget sweeps, or negative controls.
- The paper is short and framed as a narrow mechanism note.
- Existing docs/status files must be updated only after final PDF verification.

## Target Experiment

Build a deterministic RAM-light suite where a planner repeatedly encounters embodied counterexamples caused by false affordances, aliased states, contact mismatch, blocked passages, slipping supports, stale assumptions, tool failures, or changed goals. Each compact condition row will aggregate over guard policies while representing many guard/split/seed/horizon/budget/alias/reroll trials.

Factor grid:

- 24 planning domain families: false shortcut, blocked passage, slippery support, movable obstacle, tool precondition, grasp precondition, latch dependency, door hinge limit, cable snag, fragile support, narrow passage, shelf occlusion, bin clutter, peg alignment, drawer friction, handle ambiguity, push blockage, pull detachment, support collapse, handoff mismatch, conveyor drift, fixture tolerance, battery constraint, and multi-room recovery.
- 14 counterexample families: impossible transition, wrong precondition, hidden contact, stochastic slip, perception alias, tool infeasibility, nonstationary obstacle, stale patch, overblocked alternative, underblocked repeat, delayed consequence, multi-step dependency, reversible failure, and irreversible failure.
- 8 planner families: breadth-first symbolic planner, weighted A-star, anytime repair planner, sampling task-motion planner, model-predictive replanner, optimistic learned-model planner, risk-averse planner, and hybrid symbolic-continuous planner.
- 10 repair mechanisms: no repair, prediction-centric update, uncertainty penalty, action blacklist, global retraining proxy, robust replanning, exact CCRA, learned-guard CCRA, CCRA with retirement, and oracle guard CCRA.
- 8 guard policies represented inside each row: exact, under-scoped, over-scoped, aliased, learned-low-recall, learned-low-precision, budget-clipped, and stale-retired.
- 9 stress settings: clean, descriptor noise, partial observability, horizon extension, nonstationary transition, action-cost shift, planner-heuristic bias, multiple counterexamples, and adversarial guard overlap.
- 6 train/test splits.
- 13 seeds.
- 6 horizon lengths.
- 5 patch budgets.
- 4 alias levels.
- 30 deterministic rerolls per represented condition.

Actual compact rows should be over domain, counterexample family, planner, repair mechanism, and stress. Guard policies are represented inside each row and summarized separately to keep `condition_metrics.csv` below GitHub's 100 MB hard limit. The represented evaluation count should exceed 500 billion checks while the stored outputs remain compact.

## Baselines

Required baselines:

- No repair.
- Prediction-centric model update.
- Uncertainty penalty or confidence-weighted planning.
- Action blacklist.
- Global retraining proxy.
- Robust replanning with conservative transition costs.
- Exact CCRA.
- Learned-guard CCRA.
- CCRA with patch retirement.
- Oracle guard CCRA.

The final story must not depend on exact CCRA alone. It must show where guard quality, stale patch retirement, and planner cost determine whether repair actually improves recoverability.

## Ablations

- Remove planner-facing patch but keep counterexample memory.
- Keep patch but remove guard precision.
- Keep exact guard but remove patch retirement.
- Clip patch budget.
- Increase horizon length.
- Increase state aliasing.
- Increase planner heuristic bias toward the failed shortcut.
- Swap repair mechanism while holding planner constant.
- Swap planner while holding repair mechanism constant.
- Compare model prediction loss against repeated-counterexample rate.
- Separate single-counterexample and multi-counterexample regimes.
- Negative controls where prediction-centric updates are sufficient.

## Stress Tests

- Guard under-scope and over-scope.
- Partial observability and state aliasing.
- Nonstationary transitions that make old patches stale.
- Multi-counterexample episodes with interacting repairs.
- Planner heuristic bias that keeps preferring a known false shortcut.
- Horizon extension where repair cost grows with search depth.
- Patch-budget pressure where the system must retire or merge patches.
- Adversarial guard overlap where valid alternatives look similar to failed transitions.
- Negative controls with no repeated false affordance.

## Figures And Tables

Required figures:

1. Recoverability map: domain families by counterexample families with repeated-failure pressure.
2. Baseline recoverability heatmap across repair mechanisms and stress settings.
3. Prediction loss versus repeated-counterexample rate scatter.
4. Guard precision/recall versus success and blocked-valid-transition rate.
5. Planner expansion cost versus recoverability tradeoff.
6. Stale-patch regret over patch-budget and nonstationarity stresses.

Required tables:

1. Scale table with factor counts and represented evaluations.
2. Main repair-mechanism performance table.
3. Guard-policy summary table.
4. Stress summary table.
5. Planner-family summary table.
6. Domain-family summary table.
7. Counterexample-family summary table.
8. Patch-budget and stale-retirement table.
9. V2 guard-scope reconciliation table.
10. Negative-control table.

## Writing Expansion

The manuscript should become a final 25+ page paper with:

- Precise definition of robotic plan recoverability.
- Formal CCRA mechanism with guard scope, patch support, patch priority, and retirement.
- Clear distinction between prediction quality and recoverability.
- Full experiment protocol and deterministic generation details.
- Strong baseline descriptions.
- Results on repeated counterexamples, recovery latency, blocked valid transitions, search expansions, stale-patch regret, and model loss.
- Guard-scope and patch-retirement ablations.
- Failure cases and negative controls.
- Reconciliation with the v2 guard-scope stress.
- Limitations that state the suite is synthetic and guard policies are designed.
- Reproducibility and implementation appendices.

No padding. The extra pages must come from methods, results, ablations, figures, tables, safety/reliability analysis, and audit details.

## RAM-Light Execution Strategy

- Use a deterministic Python runner with standard library, numpy, and matplotlib.
- Stream compact condition rows to CSV.
- Aggregate guard-policy statistics inside each compact row and also emit separate guard summaries.
- Keep only group sums and counts in memory.
- Avoid raw per-trial dumps.
- Generate all figures from aggregate outputs.
- Run sequentially.

## Final Acceptance Checklist

Do not move to Paper44 until all items pass:

- This execution plan exists before code/manuscript edits.
- Full-scale runner completes and validates expected row counts.
- Guard-scope, stale-patch, patch-budget, and planner-cost stresses are included.
- Strong baselines are included.
- Results show recoverability advantages and guard-scope limits, not only episode success.
- Final manuscript is at least 25 pages.
- `C:/Users/wangz/Downloads/43.pdf` exists only after final build.
- Local `paper/main.pdf` is removed after canonical export.
- Final PDF text contains full-scale markers and presents v3 as the current decision.
- Final PDF is rendered to PNG pages under `tmp/pdfs/` and visually checked.
- LaTeX logs have no unresolved references/citations and no damaging overfull boxes.
- Docs/status files are updated to final v3/full-scale status.
- Git diff checks pass.
- Changes are committed and pushed before starting Paper44.

## Final Outcome

- Full-scale runner completed.
- Compact condition rows: 241,920.
- Represented evaluations: 543,449,088,000.
- Final manuscript: 25 pages.
- Canonical PDF: `C:/Users/wangz/Downloads/43.pdf`.
- Canonical SHA-256: `196DA3F15CE1C0EF79D88FD62301606E9D6BCFC36D12F124D17D68F27A1FC348`.
- Local `paper/main.pdf` removed after export.
- Canonical Downloads PDF rendered and visually checked.
- VLA-style visible link-box QA completed on pages 1, 4, 5, and 8, with 34 green citation boxes, 1 red internal-reference box, and 35 visible borders.
