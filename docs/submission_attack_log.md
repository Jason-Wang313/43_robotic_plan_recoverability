# Submission Attack Log

## Attack: exact guard assumption

Question: Does CCRA still prevent repeated failure if guards miss some false transitions?

Result: under-scoped CCRA falls to 0.859 success.

Decision impact: narrows the paper to calibrated guard scope.

## Attack: over-scoped repair

Question: Does broad repair block valid alternatives?

Result: over-scoped CCRA keeps 1.000 success but raises mean expansions to 2.746 versus 2.008 for exact guards.

Decision impact: guard scope must be a central limitation.

## Attack: real-robot readiness

Question: Is there hardware, perception, or automatic guard learning?

Result: no.

Decision impact: workshop-only.
