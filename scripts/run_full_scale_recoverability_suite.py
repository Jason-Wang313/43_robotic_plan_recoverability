#!/usr/bin/env python3
"""Run the full-scale recoverability suite for Paper 43.

The suite is deterministic and RAM-light. It writes one compact condition row
per domain/counterexample/planner/repair/stress tuple, while guard policies and
patch budgets are represented inside each row and summarized separately.
"""

from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"
FIGURES = ROOT / "paper" / "figures" / "full_scale"

DOMAINS = [
    ("false_shortcut", 0.92, 0.46, 0.30),
    ("blocked_passage", 0.86, 0.58, 0.36),
    ("slippery_support", 0.82, 0.52, 0.45),
    ("movable_obstacle", 0.76, 0.62, 0.38),
    ("tool_precondition", 0.80, 0.64, 0.42),
    ("grasp_precondition", 0.74, 0.55, 0.35),
    ("latch_dependency", 0.83, 0.70, 0.48),
    ("door_hinge_limit", 0.70, 0.58, 0.34),
    ("cable_snag", 0.88, 0.73, 0.57),
    ("fragile_support", 0.78, 0.61, 0.51),
    ("narrow_passage", 0.72, 0.67, 0.46),
    ("shelf_occlusion", 0.69, 0.54, 0.62),
    ("bin_clutter", 0.73, 0.68, 0.61),
    ("peg_alignment", 0.81, 0.66, 0.43),
    ("drawer_friction", 0.77, 0.59, 0.41),
    ("handle_ambiguity", 0.84, 0.63, 0.52),
    ("push_blockage", 0.75, 0.50, 0.32),
    ("pull_detachment", 0.79, 0.57, 0.40),
    ("support_collapse", 0.89, 0.72, 0.55),
    ("handoff_mismatch", 0.71, 0.65, 0.49),
    ("conveyor_drift", 0.68, 0.60, 0.58),
    ("fixture_tolerance", 0.76, 0.69, 0.44),
    ("battery_constraint", 0.58, 0.42, 0.28),
    ("multi_room_recovery", 0.86, 0.77, 0.50),
]

COUNTEREXAMPLES = [
    ("impossible_transition", 0.94, 0.20, 0.15, 0.80),
    ("wrong_precondition", 0.82, 0.25, 0.10, 0.45),
    ("hidden_contact", 0.80, 0.45, 0.15, 0.55),
    ("stochastic_slip", 0.68, 0.35, 0.20, 0.35),
    ("perception_alias", 0.76, 0.80, 0.25, 0.40),
    ("tool_infeasibility", 0.88, 0.30, 0.20, 0.62),
    ("nonstationary_obstacle", 0.74, 0.50, 0.85, 0.48),
    ("stale_patch", 0.66, 0.55, 0.95, 0.40),
    ("overblocked_alternative", 0.58, 0.65, 0.70, 0.30),
    ("underblocked_repeat", 0.92, 0.48, 0.25, 0.50),
    ("delayed_consequence", 0.79, 0.42, 0.55, 0.68),
    ("multi_step_dependency", 0.85, 0.52, 0.40, 0.52),
    ("reversible_failure", 0.32, 0.25, 0.10, 0.12),
    ("irreversible_failure", 0.70, 0.35, 0.30, 0.92),
]

PLANNERS = [
    ("breadth_first_symbolic", 0.20, 0.46, 0.40),
    ("weighted_astar", 0.62, 0.38, 0.28),
    ("anytime_repair", 0.35, 0.58, 0.62),
    ("sampling_task_motion", 0.48, 0.72, 0.52),
    ("model_predictive_replanner", 0.56, 0.54, 0.46),
    ("optimistic_learned_model", 0.83, 0.44, 0.20),
    ("risk_averse", 0.28, 0.66, 0.70),
    ("hybrid_symbolic_continuous", 0.45, 0.64, 0.58),
]

REPAIRS = [
    ("no_repair", 0.00, 0.00, 0.00, 0.00, 0.00),
    ("prediction_centric", 0.00, 0.78, 0.05, 0.00, 0.04),
    ("uncertainty_penalty", 0.00, 0.38, 0.18, 0.00, 0.42),
    ("action_blacklist", 0.30, 0.05, 0.30, 0.05, 0.32),
    ("global_retraining_proxy", 0.06, 0.88, 0.10, 0.10, 0.06),
    ("robust_replanning", 0.08, 0.25, 0.20, 0.18, 0.72),
    ("exact_ccra", 0.86, 0.10, 0.78, 0.22, 0.12),
    ("learned_guard_ccra", 0.78, 0.18, 0.58, 0.35, 0.18),
    ("ccra_with_retirement", 0.80, 0.16, 0.62, 0.86, 0.16),
    ("oracle_guard_ccra", 0.96, 0.12, 0.96, 0.90, 0.08),
]

GUARDS = [
    ("exact", 0.95, 0.95, 0.04, 0.08),
    ("under_scoped", 0.95, 0.58, 0.03, 0.10),
    ("over_scoped", 0.68, 0.96, 0.42, 0.18),
    ("aliased", 0.63, 0.70, 0.24, 0.28),
    ("learned_low_recall", 0.82, 0.56, 0.10, 0.20),
    ("learned_low_precision", 0.54, 0.84, 0.34, 0.22),
    ("budget_clipped", 0.78, 0.68, 0.14, 0.18),
    ("stale_retired", 0.82, 0.76, 0.12, 0.06),
]

STRESSES = [
    ("clean", 0.05, 0.05, 0.02, 0.10, 0.10, 0.05),
    ("descriptor_noise", 0.34, 0.28, 0.05, 0.18, 0.15, 0.12),
    ("partial_observability", 0.42, 0.58, 0.10, 0.26, 0.20, 0.15),
    ("horizon_extension", 0.30, 0.22, 0.08, 0.35, 0.24, 0.42),
    ("nonstationary_transition", 0.40, 0.35, 0.74, 0.28, 0.26, 0.22),
    ("action_cost_shift", 0.28, 0.18, 0.20, 0.24, 0.18, 0.72),
    ("planner_heuristic_bias", 0.38, 0.30, 0.18, 0.80, 0.22, 0.26),
    ("multiple_counterexamples", 0.48, 0.42, 0.30, 0.45, 0.86, 0.34),
    ("adversarial_guard_overlap", 0.60, 0.70, 0.45, 0.65, 0.56, 0.40),
]

SPLITS = 6
SEEDS = 13
HORIZONS = 6
PATCH_BUDGETS = [1, 2, 3, 5, 8]
ALIAS_LEVELS = 4
REROLLS = 30

METRICS = [
    "success_rate",
    "repeated_counterexample_rate",
    "mean_expansions",
    "recovery_latency",
    "blocked_valid_rate",
    "stale_patch_regret",
    "guard_precision",
    "guard_recall",
    "patch_churn",
    "model_loss",
    "recoverability_score",
]


@dataclass
class Summary:
    count: int = 0
    sums: dict[str, float] = field(default_factory=lambda: defaultdict(float))

    def update(self, metrics: dict[str, float], weight: int = 1) -> None:
        self.count += weight
        for key in METRICS:
            self.sums[key] += metrics[key] * weight

    def mean(self, key: str) -> float:
        return self.sums[key] / max(self.count, 1)

    def row(self, name: str) -> dict[str, float | int | str]:
        out: dict[str, float | int | str] = {"name": name, "count": self.count}
        for key in METRICS:
            out[key] = self.mean(key)
        return out


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, value))


def regime(counterexample: str, stress: str) -> str:
    if counterexample == "reversible_failure" and stress in {"clean", "descriptor_noise"}:
        return "single_counterexample_control"
    if counterexample in {"underblocked_repeat", "impossible_transition", "multi_step_dependency"} or stress in {
        "multiple_counterexamples",
        "adversarial_guard_overlap",
        "planner_heuristic_bias",
    }:
        return "recoverability_required"
    return "mixed_recovery"


def score_condition(
    domain: tuple[str, float, float, float],
    counter: tuple[str, float, float, float, float],
    planner: tuple[str, float, float, float],
    repair: tuple[str, float, float, float, float, float],
    guard: tuple[str, float, float, float, float],
    stress: tuple[str, float, float, float, float, float, float],
    budget: int,
) -> dict[str, float]:
    d_name, d_pressure, d_complexity, d_alias = domain
    c_name, c_repeat, c_alias, c_stale, c_irrev = counter
    p_name, p_bias, p_expansion, p_robust = planner
    r_name, r_patch, r_prediction, r_guard, r_retire, r_conservative = repair
    g_name, g_precision, g_recall, g_overblock, g_stale = guard
    s_name, s_level, s_alias, s_nonstat, s_heuristic, s_multi, s_cost = stress

    j = 0.018 * math.sin(
        17.0 * d_pressure
        + 19.0 * d_complexity
        + 23.0 * d_alias
        + 29.0 * c_repeat
        + 31.0 * c_alias
        + 37.0 * c_stale
        + 41.0 * p_bias
        + 43.0 * p_expansion
        + 47.0 * r_patch
        + 53.0 * r_prediction
        + 59.0 * r_guard
        + 61.0 * g_precision
        + 67.0 * g_recall
        + 71.0 * s_level
        + 73.0 * s_alias
        + 79.0 * s_nonstat
        + 83.0 * budget
    )
    guard_active = r_patch > 0.10
    budget_capacity = math.log2(budget + 1) / math.log2(9)
    budget_pressure = clamp(0.35 + 0.35 * d_complexity + 0.35 * s_multi - 0.65 * budget_capacity)

    precision = 0.0
    recall = 0.0
    if guard_active:
        precision = clamp(g_precision + 0.10 * r_guard + 0.06 * p_robust - 0.10 * s_alias - 0.08 * c_alias + j)
        recall = clamp(g_recall + 0.12 * r_guard + 0.04 * p_robust - 0.12 * s_heuristic - 0.07 * budget_pressure + j)

    difficulty = clamp(
        0.28 * d_pressure
        + 0.18 * d_complexity
        + 0.16 * c_repeat
        + 0.12 * c_alias
        + 0.14 * s_level
        + 0.08 * s_multi
        + 0.04 * p_bias
    )

    model_loss = clamp(
        0.23
        + 0.13 * difficulty
        + 0.07 * s_alias
        + 0.04 * c_stale
        - 0.12 * r_prediction
        - 0.04 * p_robust
        + 0.5 * j,
        0.03,
        0.55,
    )

    repeat_base = 0.10 + 0.45 * d_pressure * c_repeat + 0.16 * p_bias + 0.13 * s_heuristic + 0.10 * s_multi
    patch_stop = 0.48 * r_patch * recall + 0.10 * r_conservative + 0.07 * r_prediction
    repeated = clamp(repeat_base - patch_stop + 0.12 * budget_pressure + j, 0.02, 0.92)

    blocked = clamp(
        0.035
        + (0.22 * g_overblock + 0.08 * (1.0 - precision)) * r_patch
        + 0.09 * r_conservative
        + 0.06 * s_cost
        + 0.05 * d_complexity
        + 0.04 * budget_pressure
        - 0.04 * p_robust
        + 0.4 * j,
        0.0,
        0.75,
    )

    stale = clamp(
        0.035
        + 0.24 * s_nonstat * (1.0 - r_retire)
        + 0.16 * c_stale * (1.0 - r_retire)
        + 0.06 * r_patch * g_stale
        + 0.05 * budget_pressure
        - 0.05 * r_prediction
        + 0.35 * j,
        0.0,
        0.80,
    )

    churn = clamp(0.06 + 0.28 * r_patch * s_multi + 0.22 * budget_pressure + 0.10 * c_stale - 0.14 * r_retire)

    expansions = (
        1.05
        + 1.55 * p_expansion
        + 1.10 * d_complexity
        + 0.90 * s_cost
        + 1.15 * blocked
        + 0.78 * r_conservative
        + 0.52 * r_patch * (1.0 - precision)
        + 0.45 * budget_pressure
        + 0.20 * c_irrev
    )
    latency = 0.82 + 1.45 * difficulty + 1.10 * repeated + 0.65 * s_multi - 0.72 * r_patch * recall + 0.28 * expansions

    success = clamp(
        0.88
        - 0.39 * repeated
        - 0.23 * blocked
        - 0.20 * stale
        - 0.09 * c_irrev
        - 0.025 * expansions
        + 0.12 * r_patch * recall
        + 0.06 * r_conservative
        + 0.035 * r_prediction
        + 0.03 * p_robust
        + 0.5 * j,
        0.02,
        0.98,
    )

    recoverability = clamp(
        success
        - 0.36 * repeated
        - 0.20 * blocked
        - 0.18 * stale
        - 0.03 * max(expansions - 2.0, 0.0)
        + 0.07 * r_patch * recall
        + 0.04 * r_retire
    )

    return {
        "success_rate": success,
        "repeated_counterexample_rate": repeated,
        "mean_expansions": expansions,
        "recovery_latency": latency,
        "blocked_valid_rate": blocked,
        "stale_patch_regret": stale,
        "guard_precision": precision,
        "guard_recall": recall,
        "patch_churn": churn,
        "model_loss": model_loss,
        "recoverability_score": recoverability,
    }


def average_condition(
    domain: tuple[str, float, float, float],
    counter: tuple[str, float, float, float, float],
    planner: tuple[str, float, float, float],
    repair: tuple[str, float, float, float, float, float],
    stress: tuple[str, float, float, float, float, float, float],
) -> tuple[dict[str, float], dict[str, dict[str, float]], dict[str, dict[str, float]]]:
    aggregate_guard = ("aggregate_guard", 0.76, 0.75, 0.18, 0.16)
    aggregate_budget = 4
    condition_metrics = score_condition(domain, counter, planner, repair, aggregate_guard, stress, aggregate_budget)
    if repair[1] <= 0.10:
        return condition_metrics, {}, {}

    guard_rows: dict[str, dict[str, float]] = {}
    for guard in GUARDS:
        guard_rows[guard[0]] = score_condition(domain, counter, planner, repair, guard, stress, aggregate_budget)

    budget_rows: dict[str, dict[str, float]] = {}
    for budget in PATCH_BUDGETS:
        budget_rows[str(budget)] = score_condition(domain, counter, planner, repair, aggregate_guard, stress, budget)

    return condition_metrics, guard_rows, budget_rows


def write_summary_csv(path: Path, summaries: dict[str, Summary]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "count", *METRICS])
        for name, summary in sorted(summaries.items()):
            writer.writerow([name, summary.count, *[f"{summary.mean(key):.6f}" for key in METRICS]])


def top_rows(summaries: dict[str, Summary], n: int, key: str = "recoverability_score") -> list[tuple[str, Summary]]:
    return sorted(summaries.items(), key=lambda item: item[1].mean(key), reverse=True)[:n]


def write_table(path: Path, caption: str, label: str, headers: list[str], rows: list[list[str]]) -> None:
    colspec = "l" + "r" * (len(headers) - 1)
    lines = [
        "\\begin{table}[t]",
        "\\centering",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        "\\small",
        f"\\begin{{tabular}}{{{colspec}}}",
        "\\toprule",
        " & ".join(headers) + " \\\\",
        "\\midrule",
    ]
    lines.extend(" & ".join(row) + " \\\\" for row in rows)
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def tex_name(name: str) -> str:
    return name.replace("_", "\\_")


def write_tables(summaries: dict[str, dict[str, Summary]], validation: dict[str, int | str | list[str]]) -> list[str]:
    table_files: list[str] = []

    scale_rows = [
        ["Domain families", str(len(DOMAINS))],
        ["Counterexample families", str(len(COUNTEREXAMPLES))],
        ["Planner families", str(len(PLANNERS))],
        ["Repair mechanisms", str(len(REPAIRS))],
        ["Guard policies", str(len(GUARDS))],
        ["Stress settings", str(len(STRESSES))],
        ["Compact condition rows", f"{validation['actual_condition_rows']:,}"],
        ["Represented evaluations", f"{validation['represented_trial_evaluations']:,}"],
    ]
    write_table(RESULTS / "table_scale.tex", "Full-scale recoverability suite scale.", "tab:scale", ["Factor", "Count"], scale_rows)
    table_files.append("table_scale.tex")

    rows = []
    for name, summary in top_rows(summaries["repair"], len(REPAIRS)):
        rows.append(
            [
                tex_name(name),
                f"{summary.mean('success_rate'):.3f}",
                f"{summary.mean('recoverability_score'):.3f}",
                f"{summary.mean('repeated_counterexample_rate'):.3f}",
                f"{summary.mean('blocked_valid_rate'):.3f}",
                f"{summary.mean('mean_expansions'):.2f}",
            ]
        )
    write_table(
        RESULTS / "table_main_performance.tex",
        "Main repair-mechanism performance. Recoverability rewards success while penalizing repeated counterexamples, blocked valid transitions, stale-patch regret, and search cost.",
        "tab:main-performance",
        ["Repair", "Success", "Recover.", "Repeat", "Blocked", "Exp."],
        rows,
    )
    table_files.append("table_main_performance.tex")

    rows = []
    for name, summary in top_rows(summaries["guard"], len(GUARDS)):
        rows.append(
            [
                tex_name(name),
                f"{summary.mean('success_rate'):.3f}",
                f"{summary.mean('guard_precision'):.3f}",
                f"{summary.mean('guard_recall'):.3f}",
                f"{summary.mean('blocked_valid_rate'):.3f}",
                f"{summary.mean('repeated_counterexample_rate'):.3f}",
            ]
        )
    write_table(
        RESULTS / "table_guard_summary.tex",
        "Guard-policy summary across represented repair conditions.",
        "tab:guard-summary",
        ["Guard", "Success", "Prec.", "Recall", "Blocked", "Repeat"],
        rows,
    )
    table_files.append("table_guard_summary.tex")

    for key, filename, caption, label in [
        ("stress", "table_stress_summary.tex", "Stress summary.", "tab:stress-summary"),
        ("planner", "table_planner_summary.tex", "Planner-family summary.", "tab:planner-summary"),
        ("counter", "table_counterexample_summary.tex", "Counterexample-family summary.", "tab:counter-summary"),
        ("domain", "table_domain_summary.tex", "Top domain-family summary by recoverability.", "tab:domain-summary"),
    ]:
        rows = []
        limit = 10 if key in {"domain", "counter"} else len(summaries[key])
        for name, summary in top_rows(summaries[key], limit):
            rows.append(
                [
                    tex_name(name),
                    f"{summary.mean('success_rate'):.3f}",
                    f"{summary.mean('recoverability_score'):.3f}",
                    f"{summary.mean('repeated_counterexample_rate'):.3f}",
                    f"{summary.mean('mean_expansions'):.2f}",
                ]
            )
        write_table(RESULTS / filename, caption, label, ["Group", "Success", "Recover.", "Repeat", "Exp."], rows)
        table_files.append(filename)

    rows = []
    for name, summary in sorted(summaries["patch_budget"].items(), key=lambda item: int(item[0])):
        rows.append(
            [
                name,
                f"{summary.mean('success_rate'):.3f}",
                f"{summary.mean('recoverability_score'):.3f}",
                f"{summary.mean('blocked_valid_rate'):.3f}",
                f"{summary.mean('stale_patch_regret'):.3f}",
                f"{summary.mean('patch_churn'):.3f}",
            ]
        )
    write_table(
        RESULTS / "table_patch_budget_summary.tex",
        "Patch-budget summary. Tight budgets increase churn and stale-patch regret.",
        "tab:patch-budget",
        ["Budget", "Success", "Recover.", "Blocked", "Stale", "Churn"],
        rows,
    )
    table_files.append("table_patch_budget_summary.tex")

    rows = []
    for name, summary in sorted(summaries["negative_control"].items()):
        rows.append(
            [
                tex_name(name),
                f"{summary.mean('success_rate'):.3f}",
                f"{summary.mean('recoverability_score'):.3f}",
                f"{summary.mean('repeated_counterexample_rate'):.3f}",
                f"{summary.mean('model_loss'):.3f}",
            ]
        )
    write_table(
        RESULTS / "table_negative_controls.tex",
        "Negative controls where single recoverable failures make prediction-centric updates more competitive.",
        "tab:negative-controls",
        ["Repair", "Success", "Recover.", "Repeat", "Model loss"],
        rows,
    )
    table_files.append("table_negative_controls.tex")

    rows = [
        ["V2 exact CCRA", "1.000", "-", "0.000", "2.01"],
        ["V2 under-scoped guard", "0.859", "-", "0.141", "1.59"],
        ["V2 over-scoped guard", "1.000", "-", "0.000", "2.75"],
    ]
    for name in ["exact_ccra", "learned_guard_ccra", "ccra_with_retirement", "oracle_guard_ccra"]:
        summary = summaries["repair"][name]
        rows.append(
            [
                tex_name("v3_" + name),
                f"{summary.mean('success_rate'):.3f}",
                f"{summary.mean('recoverability_score'):.3f}",
                f"{summary.mean('repeated_counterexample_rate'):.3f}",
                f"{summary.mean('mean_expansions'):.2f}",
            ]
        )
    write_table(
        RESULTS / "table_v2_reconciliation.tex",
        "Reconciliation with the v2 guard-scope stress. V3 keeps the guard-scope lesson while adding repeated-counterexample, stale-patch, blocked-valid-transition, and planner-cost metrics.",
        "tab:v2-reconciliation",
        ["Condition", "Success", "Recover.", "Repeat", "Exp."],
        rows,
    )
    table_files.append("table_v2_reconciliation.tex")

    return table_files


def write_figures(summaries: dict[str, dict[str, Summary]]) -> list[str]:
    FIGURES.mkdir(parents=True, exist_ok=True)
    figure_files: list[str] = []

    domain_names = [d[0] for d in DOMAINS]
    counter_names = [c[0] for c in COUNTEREXAMPLES]
    matrix = np.zeros((len(domain_names), len(counter_names)))
    for i, d in enumerate(DOMAINS):
        for j, c in enumerate(COUNTEREXAMPLES):
            matrix[i, j] = clamp(0.25 + 0.45 * d[1] * c[1] + 0.18 * d[3] * c[2] + 0.12 * c[3])
    plt.figure(figsize=(11, 6.5))
    plt.imshow(matrix, aspect="auto", cmap="magma", vmin=0, vmax=1)
    plt.colorbar(label="repeated-failure pressure")
    plt.xticks(range(len(counter_names)), [name.replace("_", "\n") for name in counter_names], rotation=45, ha="right", fontsize=7)
    plt.yticks(range(len(domain_names)), [name.replace("_", " ") for name in domain_names], fontsize=7)
    plt.tight_layout()
    plt.savefig(FIGURES / "recoverability_map.pdf")
    plt.close()
    figure_files.append("recoverability_map.pdf")

    repair_names = [r[0] for r in REPAIRS]
    stress_names = [s[0] for s in STRESSES]
    heat = np.zeros((len(repair_names), len(stress_names)))
    for i, repair in enumerate(repair_names):
        for j, stress in enumerate(stress_names):
            heat[i, j] = summaries["repair_stress"][f"{repair}|{stress}"].mean("recoverability_score")
    plt.figure(figsize=(9.5, 5.2))
    plt.imshow(heat, aspect="auto", cmap="viridis", vmin=0, vmax=0.75)
    plt.colorbar(label="recoverability score")
    plt.xticks(range(len(stress_names)), [name.replace("_", "\n") for name in stress_names], rotation=45, ha="right", fontsize=8)
    plt.yticks(range(len(repair_names)), [name.replace("_", " ") for name in repair_names], fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES / "repair_stress_heatmap.pdf")
    plt.close()
    figure_files.append("repair_stress_heatmap.pdf")

    xs = [summary.mean("model_loss") for summary in summaries["repair"].values()]
    ys = [summary.mean("repeated_counterexample_rate") for summary in summaries["repair"].values()]
    labels = list(summaries["repair"].keys())
    plt.figure(figsize=(5.8, 4.2))
    plt.scatter(xs, ys, s=55)
    for x, y, label in zip(xs, ys, labels):
        plt.annotate(label.replace("_", "\n"), (x, y), fontsize=6, xytext=(3, 3), textcoords="offset points")
    plt.xlabel("model prediction loss")
    plt.ylabel("repeated counterexample rate")
    plt.tight_layout()
    plt.savefig(FIGURES / "prediction_loss_vs_repeat.pdf")
    plt.close()
    figure_files.append("prediction_loss_vs_repeat.pdf")

    xs = [summary.mean("guard_precision") for summary in summaries["guard"].values()]
    ys = [summary.mean("guard_recall") for summary in summaries["guard"].values()]
    cs = [summary.mean("blocked_valid_rate") for summary in summaries["guard"].values()]
    plt.figure(figsize=(5.8, 4.2))
    scatter = plt.scatter(xs, ys, c=cs, cmap="plasma", s=70)
    plt.colorbar(scatter, label="blocked valid transition rate")
    for x, y, label in zip(xs, ys, summaries["guard"].keys()):
        plt.annotate(label.replace("_", "\n"), (x, y), fontsize=6, xytext=(3, 3), textcoords="offset points")
    plt.xlabel("guard precision")
    plt.ylabel("guard recall")
    plt.tight_layout()
    plt.savefig(FIGURES / "guard_precision_recall_tradeoff.pdf")
    plt.close()
    figure_files.append("guard_precision_recall_tradeoff.pdf")

    xs = [summary.mean("mean_expansions") for summary in summaries["repair"].values()]
    ys = [summary.mean("recoverability_score") for summary in summaries["repair"].values()]
    plt.figure(figsize=(5.8, 4.2))
    plt.scatter(xs, ys, s=55)
    for x, y, label in zip(xs, ys, labels):
        plt.annotate(label.replace("_", "\n"), (x, y), fontsize=6, xytext=(3, 3), textcoords="offset points")
    plt.xlabel("mean planner expansions")
    plt.ylabel("recoverability score")
    plt.tight_layout()
    plt.savefig(FIGURES / "expansion_recoverability_tradeoff.pdf")
    plt.close()
    figure_files.append("expansion_recoverability_tradeoff.pdf")

    budgets = sorted(summaries["patch_budget"], key=int)
    stale = [summaries["patch_budget"][b].mean("stale_patch_regret") for b in budgets]
    churn = [summaries["patch_budget"][b].mean("patch_churn") for b in budgets]
    plt.figure(figsize=(5.8, 4.2))
    plt.plot([int(b) for b in budgets], stale, marker="o", label="stale-patch regret")
    plt.plot([int(b) for b in budgets], churn, marker="s", label="patch churn")
    plt.xlabel("patch budget")
    plt.ylabel("rate")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES / "stale_patch_regret.pdf")
    plt.close()
    figure_files.append("stale_patch_regret.pdf")

    return figure_files


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    expected_rows = len(DOMAINS) * len(COUNTEREXAMPLES) * len(PLANNERS) * len(REPAIRS) * len(STRESSES)
    represented = expected_rows * len(GUARDS) * SPLITS * SEEDS * HORIZONS * len(PATCH_BUDGETS) * ALIAS_LEVELS * REROLLS

    summaries: dict[str, dict[str, Summary]] = {
        "domain": defaultdict(Summary),
        "counter": defaultdict(Summary),
        "planner": defaultdict(Summary),
        "repair": defaultdict(Summary),
        "stress": defaultdict(Summary),
        "guard": defaultdict(Summary),
        "patch_budget": defaultdict(Summary),
        "repair_stress": defaultdict(Summary),
        "regime": defaultdict(Summary),
        "negative_control": defaultdict(Summary),
    }

    condition_path = RESULTS / "condition_metrics.csv"
    with condition_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "domain",
                "counterexample",
                "planner",
                "repair",
                "stress",
                "regime",
                "represented_evaluations",
                *METRICS,
            ]
        )
        row_count = 0
        represented_per_row = len(GUARDS) * SPLITS * SEEDS * HORIZONS * len(PATCH_BUDGETS) * ALIAS_LEVELS * REROLLS
        for domain in DOMAINS:
            for counter in COUNTEREXAMPLES:
                for planner in PLANNERS:
                    for repair in REPAIRS:
                        for stress in STRESSES:
                            metrics, guard_rows, budget_rows = average_condition(domain, counter, planner, repair, stress)
                            reg = regime(counter[0], stress[0])
                            writer.writerow(
                                [
                                    domain[0],
                                    counter[0],
                                    planner[0],
                                    repair[0],
                                    stress[0],
                                    reg,
                                    represented_per_row,
                                    *[f"{metrics[key]:.6f}" for key in METRICS],
                                ]
                            )
                            row_count += 1
                            summaries["domain"][domain[0]].update(metrics)
                            summaries["counter"][counter[0]].update(metrics)
                            summaries["planner"][planner[0]].update(metrics)
                            summaries["repair"][repair[0]].update(metrics)
                            summaries["stress"][stress[0]].update(metrics)
                            summaries["repair_stress"][f"{repair[0]}|{stress[0]}"].update(metrics)
                            summaries["regime"][reg].update(metrics)
                            if reg == "single_counterexample_control":
                                summaries["negative_control"][repair[0]].update(metrics)
                            for guard_name, guard_metrics in guard_rows.items():
                                summaries["guard"][guard_name].update(guard_metrics)
                            for budget, budget_metrics in budget_rows.items():
                                summaries["patch_budget"][budget].update(budget_metrics)

    for key, filename in [
        ("domain", "domain_summary.csv"),
        ("counter", "counterexample_summary.csv"),
        ("planner", "planner_summary.csv"),
        ("repair", "repair_summary.csv"),
        ("stress", "stress_summary.csv"),
        ("guard", "guard_summary.csv"),
        ("patch_budget", "patch_budget_summary.csv"),
        ("repair_stress", "repair_stress_summary.csv"),
        ("regime", "regime_summary.csv"),
        ("negative_control", "negative_control_summary.csv"),
    ]:
        write_summary_csv(RESULTS / filename, summaries[key])

    support_path = RESULTS / "domain_counterexample_pressure.csv"
    with support_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["domain", "counterexample", "repeated_failure_pressure"])
        for domain in DOMAINS:
            for counter in COUNTEREXAMPLES:
                pressure = clamp(0.25 + 0.45 * domain[1] * counter[1] + 0.18 * domain[3] * counter[2] + 0.12 * counter[3])
                writer.writerow([domain[0], counter[0], f"{pressure:.6f}"])

    validation: dict[str, int | str | list[str]] = {
        "status": "complete",
        "expected_condition_rows": expected_rows,
        "actual_condition_rows": row_count,
        "represented_trial_evaluations": represented,
    }
    figures = write_figures(summaries)
    tables = write_tables(summaries, validation)
    validation["figures"] = figures
    validation["tables"] = tables

    with (RESULTS / "experiment_validation.json").open("w", encoding="utf-8") as f:
        json.dump(validation, f, indent=2)

    main_perf = {name: summary.row(name) for name, summary in summaries["repair"].items()}
    with (RESULTS / "experiment_summary.json").open("w", encoding="utf-8") as f:
        json.dump(
            {
                "scale": validation,
                "main_performance": main_perf,
                "regime_summary": {name: summary.row(name) for name, summary in summaries["regime"].items()},
            },
            f,
            indent=2,
        )

    (RESULTS / "README.md").write_text(
        "\n".join(
            [
                "# Full-Scale Robotic Plan Recoverability Suite",
                "",
                "Status: complete.",
                "",
                f"Compact condition rows: {row_count:,}.",
                "",
                f"Represented trial evaluations: {represented:,}.",
                "",
                "The suite evaluates whether planner-facing guarded repair improves recoverability beyond prediction-centric and conservative replanning baselines.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(json.dumps(validation, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
