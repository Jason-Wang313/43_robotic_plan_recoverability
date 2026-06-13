# Claims

## Core claims

- Sparse planner-exploited transition errors can dominate embodied success more than average prediction loss.
- A guarded transition patch can stop repeated exploitation after a counterexample in a deterministic finite model.
- CCRA is distinct from system identification, residual correction, uncertainty, or verifier-only safety when the repair is consumed by the planner.
- The paper is mechanistic and diagnostic, not a claim of full real-robot state of the art.

## V2 narrowed claim

The v2 guard-scope stress shows the main dependency. Exact CCRA reaches 1.000 success, but under-scoped guards fall to 0.859 success and over-scoped guards raise mean expansions from 2.008 to 2.746. The safe claim is therefore calibrated planner-facing repair, not generic failure recovery.
