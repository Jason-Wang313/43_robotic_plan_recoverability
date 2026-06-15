# Submission Version Log

## v1

- Original recoverability probe showed CCRA success 1.000 in a small false-shortcut setting.
- Prediction-centric and no-repair baselines were included.

## v2

- Added guard-scope stress.
- Found exact guards succeed, under-scoped guards miss repeats, and over-scoped guards increase expansions.
- Recorded the result as a narrowing constraint for the next version.

## v3

- Wrote a full-scale execution plan before edits.
- Added `scripts/run_full_scale_recoverability_suite.py`.
- Generated 241,920 compact condition rows representing 543,449,088,000 evaluations.
- Rewrote the manuscript around recoverability metrics and counterexample-conditioned repair automata.
- Added full-scale tables, figures, guard policies, stress tests, patch-budget analysis, negative controls, safety, and reproducibility appendices.
- Built and visually checked the 25-page canonical PDF at `C:/Users/wangz/Downloads/43.pdf`.
- Final SHA-256: `39E6A9709EFD4D6E6960E5486FC269A42A62B9877110128FFD0819098ED3EB5C`.
