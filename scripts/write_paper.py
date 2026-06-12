#!/usr/bin/env python3
"""Write the paper tables from the experiment summary."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
RESULTS = ROOT / "results"


def fmt_pct(x: float) -> str:
    return f"{100.0 * x:.1f}\\%"


def fmt(x: float) -> str:
    return f"{x:.1f}"


def main() -> int:
    summary = json.loads((RESULTS / "summary.json").read_text(encoding="utf-8"))
    lines = [
        "\\begin{tabular}{lrrr}",
        "\\toprule",
        "Method & Success & Mean expansions & Mean cost \\\\",
        "\\midrule",
    ]
    for key, label in [
        ("no_repair", "No repair"),
        ("prediction_centric", "Prediction-centric"),
        ("ccra", "CCRA"),
    ]:
        row = summary[key]
        lines.append(
            f"{label} & {fmt_pct(float(row['success_rate']))} & {fmt(float(row['mean_expansions']))} & {fmt(float(row['mean_cost_successes']))} \\\\"
        )
    lines += ["\\bottomrule", "\\end{tabular}"]
    (PAPER / "results_table.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
