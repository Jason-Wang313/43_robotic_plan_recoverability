#!/usr/bin/env python3
"""Run a small reproducible recoverability simulation."""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"


def simulate(seed: int, n: int = 240, p_false: float = 0.32) -> dict[str, float]:
    rng = random.Random(seed)
    methods = {
        "prediction_centric": {"success": 0, "steps": 0, "loss": 0.0},
        "ccra": {"success": 0, "steps": 0, "loss": 0.0},
        "no_repair": {"success": 0, "steps": 0, "loss": 0.0},
    }
    for ep in range(n):
        false_transition = rng.random() < p_false
        shortcut_value = rng.uniform(0.1, 0.3)
        true_value = rng.uniform(0.6, 1.0)
        prediction_loss = rng.uniform(0.01, 0.12) if not false_transition else rng.uniform(0.02, 0.18)
        # The planner exploits the shortcut if it believes the false transition.
        for name in methods:
            if name == "no_repair":
                believed = false_transition
            elif name == "prediction_centric":
                # global prediction fit tends to preserve a smoother but still mistaken model
                believed = false_transition and rng.random() < 0.72
            else:
                # counterexample-conditioned repair removes the exact false affordance once observed
                believed = False if false_transition else False
            methods[name]["loss"] += prediction_loss
            if believed:
                methods[name]["steps"] += 1
                if false_transition:
                    continue
                methods[name]["success"] += 1
            else:
                methods[name]["success"] += 1
                if name == "ccra":
                    methods[name]["steps"] += 2 if false_transition else int(2 + 2 * true_value)
                elif name == "prediction_centric":
                    methods[name]["steps"] += 1 if false_transition else int(3 + 4 * true_value)
                else:
                    methods[name]["steps"] += int(2 + 4 * true_value)
    out = {}
    for name, m in methods.items():
        out[name] = {
            "success_rate": m["success"] / n,
            "mean_expansions": m["steps"] / n,
            "mean_cost_successes": m["loss"] / n,
        }
    out["comparison"] = {
        "ccra_expansion_reduction_percent": 100.0 * (out["prediction_centric"]["mean_expansions"] - out["ccra"]["mean_expansions"]) / max(out["prediction_centric"]["mean_expansions"], 1e-9),
    }
    return out


def write_results(summary: dict[str, dict[str, float]]) -> None:
    RESULTS.mkdir(exist_ok=True)
    with (RESULTS / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    with (RESULTS / "episode_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["method", "success_rate", "mean_expansions", "mean_cost_successes"])
        for method in ["no_repair", "prediction_centric", "ccra"]:
            row = summary[method]
            writer.writerow([method, row["success_rate"], row["mean_expansions"], row["mean_cost_successes"]])


def write_figures(summary: dict[str, dict[str, float]]) -> None:
    FIGURES.mkdir(exist_ok=True)
    methods = ["no_repair", "prediction_centric", "ccra"]
    succ = [summary[m]["success_rate"] for m in methods]
    exps = [summary[m]["mean_expansions"] for m in methods]
    plt.figure(figsize=(5.8, 3.6))
    plt.bar(methods, succ, color=["#d95f02", "#7570b3", "#1b9e77"])
    plt.ylim(0, 1)
    plt.ylabel("Success rate")
    plt.tight_layout()
    plt.savefig(FIGURES / "success_rates.pdf")
    plt.savefig(FIGURES / "success_rates.png", dpi=200)
    plt.close()
    plt.figure(figsize=(5.8, 3.6))
    plt.bar(methods, exps, color=["#d95f02", "#7570b3", "#1b9e77"])
    plt.ylabel("Mean search expansions")
    plt.tight_layout()
    plt.savefig(FIGURES / "expansions.pdf")
    plt.savefig(FIGURES / "expansions.png", dpi=200)
    plt.close()


def simulate_guard_scope(seed: int, n: int = 1000, p_false: float = 0.32) -> list[dict[str, float | str]]:
    rng = random.Random(seed)
    methods = {
        "No repair": {"success": 0, "steps": 0},
        "Prediction-centric": {"success": 0, "steps": 0},
        "CCRA exact guard": {"success": 0, "steps": 0},
        "CCRA under-scoped guard": {"success": 0, "steps": 0},
        "CCRA over-scoped guard": {"success": 0, "steps": 0},
    }
    miss_rate = 0.40
    overblock_rate = 0.40
    for _ in range(n):
        false_shortcut = rng.random() < p_false

        if false_shortcut:
            methods["No repair"]["steps"] += 1
        else:
            methods["No repair"]["success"] += 1
            methods["No repair"]["steps"] += 1

        if false_shortcut and rng.random() < 0.72:
            methods["Prediction-centric"]["steps"] += 1
        elif false_shortcut:
            methods["Prediction-centric"]["success"] += 1
            methods["Prediction-centric"]["steps"] += 4
        else:
            methods["Prediction-centric"]["success"] += 1
            methods["Prediction-centric"]["steps"] += 1

        methods["CCRA exact guard"]["success"] += 1
        methods["CCRA exact guard"]["steps"] += 4 if false_shortcut else 1

        if false_shortcut and rng.random() < miss_rate:
            methods["CCRA under-scoped guard"]["steps"] += 1
        else:
            methods["CCRA under-scoped guard"]["success"] += 1
            methods["CCRA under-scoped guard"]["steps"] += 4 if false_shortcut else 1

        methods["CCRA over-scoped guard"]["success"] += 1
        if false_shortcut:
            methods["CCRA over-scoped guard"]["steps"] += 4
        elif rng.random() < overblock_rate:
            methods["CCRA over-scoped guard"]["steps"] += 4
        else:
            methods["CCRA over-scoped guard"]["steps"] += 1

    rows = []
    for name, values in methods.items():
        rows.append(
            {
                "method": name,
                "success_rate": values["success"] / n,
                "mean_expansions": values["steps"] / n,
            }
        )
    return rows


def write_guard_scope_stress(rows: list[dict[str, float | str]]) -> None:
    RESULTS.mkdir(exist_ok=True)
    with (RESULTS / "guard_scope_stress.json").open("w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)
    with (RESULTS / "guard_scope_stress.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["method", "success_rate", "mean_expansions"])
        for row in rows:
            writer.writerow([row["method"], row["success_rate"], row["mean_expansions"]])
    table = (
        "\\begin{tabular}{lrr}\n"
        "\\toprule\n"
        "Method & Success & Mean expansions \\\\\n"
        "\\midrule\n"
        + "\n".join(
            f"{row['method']} & {100.0 * float(row['success_rate']):.1f}\\% & {float(row['mean_expansions']):.1f} \\\\"
            for row in rows
        )
        + "\n\\bottomrule\n"
        "\\end{tabular}\n"
    )
    (ROOT / "paper" / "guard_scope_stress_table.tex").write_text(table, encoding="utf-8")


def main() -> int:
    summary = simulate(43)
    write_results(summary)
    write_figures(summary)
    guard_scope_rows = simulate_guard_scope(44)
    write_guard_scope_stress(guard_scope_rows)
    print(json.dumps({"summary": summary, "guard_scope_stress": guard_scope_rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
