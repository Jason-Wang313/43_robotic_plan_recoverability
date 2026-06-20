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
- Final SHA-256: `196DA3F15CE1C0EF79D88FD62301606E9D6BCFC36D12F124D17D68F27A1FC348`.

## v3 visual hardening

- Rebuilt the same 25-page manuscript with visible VLA-style red/green link boxes.
- Verified affected pages 1, 4, 5, and 8 by PNG render.
