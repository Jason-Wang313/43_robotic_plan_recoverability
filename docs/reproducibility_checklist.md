# Reproducibility Checklist

- Full-scale suite command: `python scripts/run_full_scale_recoverability_suite.py`
- PDF build command: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build_pdf.ps1`
- Canonical PDF location: `C:/Users/wangz/Downloads/43.pdf`
- Canonical SHA-256: `39E6A9709EFD4D6E6960E5486FC269A42A62B9877110128FFD0819098ED3EB5C`
- Local generated paper PDF retained in repo: no.
- Full-scale validation: `results/full_scale/experiment_validation.json`
- Final artifact validation: `results/full_scale/validation.json`
- Main aggregate CSV: `results/full_scale/condition_metrics.csv`
- Summary CSVs: repair, guard, stress, planner, domain, counterexample, regime, patch budget, negative controls, and repair-stress.
- Paper tables: `results/full_scale/table_*.tex`
- Paper figures: `paper/figures/full_scale/*.pdf`
- Visual QA: canonical Downloads PDF rendered to PNG pages and checked before final cleanup.
