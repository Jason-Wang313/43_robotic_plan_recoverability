# Final Audit

Paper: 43_robotic_plan_recoverability

Decision: workshop-only

Submission-hardening version: v2

## Original positive evidence

- No repair success: 0.754.
- Prediction-centric success: 0.808.
- CCRA success: 1.000.
- CCRA mean expansions: 2.754 versus 4.463 for prediction-centric updating.
- Original interpretation: planner-facing patches can stop repeated exploitation of false affordances.

## V2 guard-scope stress

- No repair: 0.664 success, 1.000 mean expansions.
- Prediction-centric: 0.748 success, 1.252 mean expansions.
- CCRA exact guard: 1.000 success, 2.008 mean expansions.
- CCRA under-scoped guard: 0.859 success, 1.585 mean expansions.
- CCRA over-scoped guard: 1.000 success, 2.746 mean expansions.

## Audit judgment

The paper survives as a narrow workshop mechanism note. It is honest and runnable, but its result depends on exact or well-calibrated guard scope. It does not establish real-robot scalability, perception robustness, or automatic guard learning.

## Artifacts

- Paper source: `paper/main.tex`
- Original results table: `paper/results_table.tex`
- V2 stress table: `paper/guard_scope_stress_table.tex`
- Original metrics: `results/summary.json`
- V2 stress JSON: `results/guard_scope_stress.json`
- V2 stress CSV: `results/guard_scope_stress.csv`
- Experiment script: `scripts/run_experiments.py`
- Build wrapper: `scripts/build_pdf.ps1`

## PDF and repository

- Canonical PDF: `C:/Users/wangz/Downloads/43.pdf`
- Local tracked/generated PDF: removed after build
- Desktop copy: absent
- GitHub URL: `https://github.com/Jason-Wang313/43_robotic_plan_recoverability`
