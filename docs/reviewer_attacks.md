# Reviewer Attacks

1. This is just replanning.
2. This is just model learning with memory.
3. Exact guards are unrealistic.
4. Over-scoped patches can hide valid plans.
5. Under-scoped patches miss repeated failures.
6. Stale patches can make the robot conservative forever.
7. Success rate alone can hide the real tradeoff.
8. Synthetic suites can hide convenient assumptions.
9. Robust replanning may solve the problem with enough search.
10. Prediction-centric update may solve the problem with enough data.

## v3 response

Attacks 3, 4, 5, and 6 are accepted and built into the final design. The paper reports exact, under-scoped, over-scoped, aliased, learned, budget-clipped, and stale-retired guards separately.

Attacks 1, 2, 9, and 10 are addressed with baselines. Replanning, prediction-centric update, uncertainty penalties, action blacklists, global retraining proxies, and robust replanning are included.

Attack 8 remains a real limitation. The paper is explicit that the suite is synthetic and diagnostic. The hardware validation and falsification sections specify what future robot evidence must test.
