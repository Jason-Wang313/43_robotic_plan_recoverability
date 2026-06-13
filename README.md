# Robotic Plan Recoverability

Paper 43 in the robotics 60-paper batch.

## V2 hardening decision

Decision: workshop-only.

The v2 guard-scope stress narrows the claim. Exact CCRA reaches 1.000 success, but under-scoped guards fall to 0.859 success and over-scoped guards preserve success only by raising mean expansions from 2.0 to 2.7. The paper is therefore a mechanism note about planner-facing repair with calibrated guards, not a deploy-ready robotics system.

Canonical PDF: `C:/Users/wangz/Downloads/43.pdf`

## Contents

- `paper/main.tex`: ICLR-style source with the v2 hardening note.
- `paper/results_table.tex`: original recoverability probe table.
- `paper/guard_scope_stress_table.tex`: v2 guard-scope stress table.
- `results/`: summary metrics, episode results, and v2 guard-scope stress files.
- `figures/`: generated synthetic evidence figures.
- `docs/`: literature notes, novelty docs, reviewer attacks, checklists, and final audit.
- `scripts/run_experiments.py`: regenerates the original and v2 synthetic evidence.
- `scripts/build_pdf.ps1`: canonical PDF build wrapper.

## Reproduce

Run the experiments:

```powershell
python scripts/run_experiments.py
```

Build the canonical PDF:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1
```
