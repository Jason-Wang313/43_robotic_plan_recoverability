# Reviewer Attacks

- This is just online system identification.
- This is just residual learning.
- This is just MPC with a learned model.
- This is just a benchmark.
- The evidence is synthetic.
- Exact guard scope is unrealistic.
- Over-scoped repair may block valid plans.
- Under-scoped repair may miss repeated failures.

## V2 outcome

The guard-scope attacks are real and now define the paper boundary. Under-scoped CCRA reaches only 0.859 success, while over-scoped CCRA keeps 1.000 success but raises mean expansions to 2.746. The paper should be judged as a narrow mechanism note whose main open problem is calibrated guard extraction and retirement.
