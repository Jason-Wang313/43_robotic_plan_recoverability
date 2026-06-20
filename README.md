# Robotic Plan Recoverability

Paper 43 in the robotics 60-paper batch.

## Final v3 status

Status: final v3 full-scale manuscript.

Canonical PDF: `C:/Users/wangz/Downloads/43.pdf`

Canonical PDF SHA-256: `196DA3F15CE1C0EF79D88FD62301606E9D6BCFC36D12F124D17D68F27A1FC348`

The v3 paper reframes the earlier guard-scope stress into a full recoverability study. Exact guarded repair remains useful, but the final manuscript evaluates repeated counterexamples, blocked valid transitions, stale-patch regret, patch churn, planner expansions, and model loss across a large deterministic suite.

The final PDF also uses visible VLA-style link boxes: green citation boxes, red internal-reference boxes, and thin boxed borders verified on affected pages 1, 4, 5, and 8.

## Full-scale suite

- Compact condition rows: 241,920.
- Represented guard/split/seed/horizon/budget/alias/reroll evaluations: 543,449,088,000.
- Factors: 24 planning-domain families, 14 counterexample families, 8 planner families, 10 repair mechanisms, 8 guard policies, 9 stresses, 6 splits, 13 seeds, 6 horizon lengths, 5 patch budgets, 4 alias levels, and 30 rerolls.
- Final manuscript length: 25 pages.

## Contents

- `paper/main.tex`: final ICLR-style manuscript source.
- `scripts/run_full_scale_recoverability_suite.py`: deterministic RAM-light full-scale runner.
- `results/full_scale/`: generated aggregate CSVs, validation files, LaTeX tables, and suite README.
- `paper/figures/full_scale/`: generated full-scale figures.
- `scripts/build_pdf.ps1`: canonical PDF build/export wrapper.
- `docs/`: plans, audits, reviewer attacks, novelty decision, and reproducibility records.

## Reproduce

Run the full-scale suite:

```powershell
python scripts/run_full_scale_recoverability_suite.py
```

Build the canonical PDF:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build_pdf.ps1
```
