# Child Status 43

Status: workshop_only
Attempt: 1
Stage: v2_submission_hardening

Current facts:
- Literature and synthesis docs are present under `docs/`.
- Original synthetic recoverability artifacts are present under `results/` and `figures/`.
- V2 guard-scope stress artifacts are present at `results/guard_scope_stress.json`, `results/guard_scope_stress.csv`, and `paper/guard_scope_stress_table.tex`.
- Exact CCRA reaches 1.000 success in the v2 stress.
- Under-scoped guards fall to 0.859 success.
- Over-scoped guards preserve 1.000 success but raise mean expansions to 2.746 versus 2.008 for exact guards.
- Canonical PDF target: `C:/Users/wangz/Downloads/43.pdf`.
- Canonical PDF size: 161408 bytes.
- Local generated paper PDF is removed after build.
- Desktop PDF copy is absent.

Decision:
- Workshop-only. The supported contribution is planner-facing recoverability with calibrated guard scope, not real-robot readiness or automatic guard learning.

End time: 2026-06-13 09:08:23 +01:00
