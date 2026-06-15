# Final Audit

Paper: 43_robotic_plan_recoverability

Status: final v3 full-scale manuscript

## V2 lesson retained

The earlier guard-scope stress showed that exact CCRA succeeds in a small toy while under-scoped and over-scoped guards fail in different ways. The final paper keeps that lesson and makes guard scope, stale patches, blocked valid transitions, and planner cost central metrics.

## V3 contribution

The final paper tests recoverability at scale. Prediction-centric update has low model loss but high repeated-counterexample rate. Exact CCRA and CCRA with retirement reduce repeats and improve recoverability. The oracle guard result estimates headroom rather than deployable performance.

## Key artifacts

- Paper source: `paper/main.tex`
- Full-scale runner: `scripts/run_full_scale_recoverability_suite.py`
- Full-scale outputs: `results/full_scale/`
- Figures: `paper/figures/full_scale/`
- Build wrapper: `scripts/build_pdf.ps1`
- Build status: `data/build_status.json`

## Final PDF

- Canonical PDF: `C:/Users/wangz/Downloads/43.pdf`
- Pages: 25.
- File bytes: 389065.
- SHA-256: `39E6A9709EFD4D6E6960E5486FC269A42A62B9877110128FFD0819098ED3EB5C`
- Local tracked/generated PDF: removed after build.
- Render QA: canonical Downloads PDF rendered to PNG pages and contact sheet under `tmp/pdfs/` before cleanup.

## Repository

GitHub URL: `https://github.com/Jason-Wang313/43_robotic_plan_recoverability`
