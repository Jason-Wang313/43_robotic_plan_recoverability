# Reproducibility Checklist

- Full-scale suite command: `python scripts/run_full_scale_recoverability_suite.py`
- PDF build command: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build_pdf.ps1`
- Canonical PDF location: `C:/Users/wangz/Downloads/43.pdf`
- Canonical SHA-256: `196DA3F15CE1C0EF79D88FD62301606E9D6BCFC36D12F124D17D68F27A1FC348`
- Local generated paper PDF retained in repo: no.
- Full-scale validation: `results/full_scale/experiment_validation.json`
- Final artifact validation: `results/full_scale/validation.json`
- Main aggregate CSV: `results/full_scale/condition_metrics.csv`
- Summary CSVs: repair, guard, stress, planner, domain, counterexample, regime, patch budget, negative controls, and repair-stress.
- Paper tables: `results/full_scale/table_*.tex`
- Paper figures: `paper/figures/full_scale/*.pdf`
- Visual QA: canonical Downloads PDF rendered to PNG pages and checked before final cleanup.
- Link-box QA: affected pages 1, 4, 5, and 8 rendered at 160 dpi after rebuild; green citation boxes and red internal-reference box match the VLA-style boxed annotation target.
