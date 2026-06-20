# Paper 43 VLA Highlight Hardening Plan

Date: 2026-06-20

## Objective

Harden Paper 43's visible PDF link-box styling so it matches the VLA-v4 role-model PDF's professional red and green boxed callouts while preserving the final 25-page robotic plan recoverability manuscript, its full-scale benchmark, and all scientific claims.

## Current Evidence

- Canonical PDF: `C:/Users/wangz/Downloads/43.pdf`.
- Pre-change artifact existed at the canonical path and was superseded by the final rebuild recorded below.
- Current size: 389065 bytes.
- Current page count: 25.
- Current affected link pages: 1, 4, 5, and 8.
- Current link annotations: 34 green citation/link boxes and 1 red internal-reference box.
- Current border state: all 35 link annotations use border `(0, 0, 0)`, so the boxes are invisible.
- Current LaTeX source uses `\usepackage[hidelinks]{hyperref}` in `paper/main.tex`.
- Current build wrapper is `scripts/build_pdf.ps1`; it builds inside `paper/`, exports `C:/Users/wangz/Downloads/43.pdf`, and removes local `paper/main.pdf`.
- Current full-scale benchmark remains 241,920 compact condition rows and 543,449,088,000 represented evaluations.
- Pre-change pages 1, 4, 5, and 8 were rendered to `C:/Users/wangz/highlight_box_hardening/tmp/pdfs/paper43_before` at 160 dpi for baseline visual comparison.

## Role-Model Style Target

Match the VLA-v4 role model's link annotation style:

```tex
\usepackage{hyperref}
\hypersetup{
  colorlinks=false,
  pdfborder={0 0 1},
  citebordercolor={0 1 0},
  linkbordercolor={1 0 0},
  urlbordercolor={0 1 0}
}
```

Expected Paper 43 result after rebuild:

- Page count remains 25.
- All 34 citation/link annotations remain green.
- The single internal-reference link annotation remains red.
- All 35 link annotations use visible border `(0, 0, 1)`.
- No benchmark data, tables, figures, claims, or manuscript body text changes.

## Execution Plan

1. Preserve the before-render evidence for pages 1, 4, 5, and 8 until post-change QA passes.
2. Replace `\usepackage[hidelinks]{hyperref}` in `paper/main.tex` with plain `\usepackage{hyperref}` plus the VLA-v4 `\hypersetup` block above.
3. Rebuild using `scripts/build_pdf.ps1`, which exports only `C:/Users/wangz/Downloads/43.pdf`, records build metadata, and removes local `paper/main.pdf`.
4. Verify with `pypdf` that the rebuilt PDF has 25 pages, 34 green link annotations, 1 red link annotation, and 35 `(0, 0, 1)` borders.
5. Render affected post-change pages 1, 4, 5, and 8 and visually inspect the boxes for role-model-like color, line weight, alignment, spacing, and legibility.
6. Update README, child status, and tracked audit/readiness metadata with the final hash, size, and visual hardening evidence.
7. Remove Paper 43 temporary render folders after QA while preserving the shared `role_model` render.
8. Commit and push the clean repo before moving to the next paper.

## Non-Goals

- Do not rerun the benchmark.
- Do not pad content or alter the 25-page manuscript.
- Do not revise claims, tables, captions, figures, or body text unless visual QA exposes a layout defect that requires a tiny local fix.

## Final QA Result

- Rebuilt canonical PDF: `C:/Users/wangz/Downloads/43.pdf`.
- Final SHA-256: `196DA3F15CE1C0EF79D88FD62301606E9D6BCFC36D12F124D17D68F27A1FC348`.
- Final size: 389065 bytes.
- Page count remains 25.
- Annotation inventory: 34 green citation/link boxes, 1 red internal-reference box, and 35 visible `(0, 0, 1)` borders.
- Visual QA rendered pages 1, 4, 5, and 8 at 160 dpi. The boxes are thin, aligned, legible, and collision-free, matching the VLA-v4 role-model treatment.
- Local `paper/main.pdf` was removed by the build wrapper after export.
