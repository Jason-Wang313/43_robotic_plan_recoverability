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
- SHA-256: `196DA3F15CE1C0EF79D88FD62301606E9D6BCFC36D12F124D17D68F27A1FC348`
- Local tracked/generated PDF: removed after build.
- Render QA: canonical Downloads PDF rendered to PNG pages and contact sheet under `tmp/pdfs/` before cleanup.
- VLA-style link-box QA: affected pages 1, 4, 5, and 8 rendered at 160 dpi; verified 34 green citation boxes, 1 red internal-reference box, and 35 visible `(0, 0, 1)` borders with no visual collisions.

## Repository

GitHub URL: `https://github.com/Jason-Wang313/43_robotic_plan_recoverability`
