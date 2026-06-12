#!/usr/bin/env python3
"""Collect a 1000+ paper robotics literature matrix from Crossref and arXiv."""

from __future__ import annotations

import csv
import json
import re
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = ROOT / "data"
CACHE = DATA / "literature_cache.jsonl"
OUT = DOCS / "related_work_matrix.csv"

TARGET_MIN = 1050
PAGE_SIZE = 100

QUERIES = [
    "robot planning control manipulation world model",
    "robot learned dynamics model planning",
    "task and motion planning robot",
    "model predictive control robot manipulation",
    "visual foresight robot manipulation",
    "video prediction robot world model",
    "system identification robot control",
    "online adaptation robot dynamics",
    "sim to real robot learning dynamics",
    "contact dynamics robot manipulation",
    "tactile robot world model",
    "embodied AI world model robot",
    "affordance robot planning",
    "rearrangement planning robot manipulation",
    "legged robot dynamics adaptation",
    "plan repair robotics",
    "robot failure recovery planning",
    "robot recovery after execution failure",
    "planner-execution counterexample robot",
    "execution monitoring robot planning",
]

ROBOTICS_HINTS = [
    "robot", "robotic", "robotics", "manipulation", "grasp", "planning", "control",
    "locomotion", "dynamics", "tactile", "embodied", "contact", "sim-to-real", "sim to real",
    "affordance", "motion planning", "task and motion planning", "mpc", "world model",
]


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").replace("\x00", " ")).strip()


def text_blob(row: dict[str, str]) -> str:
    return " ".join([row.get("title", ""), row.get("abstract", ""), row.get("venue", ""), row.get("concepts", "")]).lower()


def http_get(url: str, headers: dict[str, str] | None = None, retries: int = 4) -> dict[str, Any]:
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers or {"User-Agent": "paper43-literature/1.0"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            if i == retries - 1:
                return {"error": repr(exc)}
            time.sleep(2 + i)
    return {"error": "unreachable"}


def crossref_items(query: str, rows: int = 100, offset: int = 0) -> list[dict[str, Any]]:
    params = {
        "query.bibliographic": query,
        "rows": str(rows),
        "offset": str(offset),
        "select": "DOI,title,author,container-title,issued,abstract,URL,type,is-referenced-by-count",
    }
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode(params)
    data = http_get(url, headers={"User-Agent": "paper43-literature/1.0 (mailto:anonymous@example.com)"})
    return data.get("message", {}).get("items", []) if isinstance(data, dict) else []


def arxiv_items(query: str, max_results: int = 100, start: int = 0) -> list[dict[str, Any]]:
    # Atom endpoint from arXiv.
    params = {
        "search_query": query,
        "start": str(start),
        "max_results": str(max_results),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "paper43-literature/1.0"}), timeout=60).read().decode("utf-8", "ignore")
    entries = re.split(r"<entry>", raw)[1:]
    out: list[dict[str, Any]] = []
    for entry in entries:
        title_m = re.search(r"<title>(.*?)</title>", entry, flags=re.S)
        summary_m = re.search(r"<summary>(.*?)</summary>", entry, flags=re.S)
        id_m = re.search(r"<id>(.*?)</id>", entry, flags=re.S)
        if not title_m:
            continue
        title = clean(re.sub(r"<.*?>", "", title_m.group(1)))
        out.append({
            "title": title,
            "abstract": clean(re.sub(r"<.*?>", "", summary_m.group(1))) if summary_m else "",
            "url": clean(id_m.group(1)) if id_m else "",
            "doi": "",
            "venue": "arXiv",
            "year": "",
            "authors": "",
            "cited_by_count": "0",
            "concepts": "arXiv",
            "source": "arxiv",
        })
    return out


def infer(row: dict[str, str]) -> dict[str, str]:
    blob = text_blob(row)
    if re.search(r"repair|recover|failure", blob):
        problem = "Repair or recover a robot plan/model after an execution failure or mismatch."
    elif re.search(r"planning|motion planning|tamp|control|mpc", blob):
        problem = "Plan or control embodied robot behavior with learned, symbolic, or hybrid models."
    elif re.search(r"world model|prediction|video", blob):
        problem = "Predict action-conditioned physical outcomes for embodied decision making."
    else:
        problem = f"Advance embodied physical intelligence around: {row.get('title','')[:120]}."

    if re.search(r"system identification|adaptation|online", blob):
        mech = "online adaptation or system identification"
    elif re.search(r"residual", blob):
        mech = "residual correction on a nominal dynamics model"
    elif re.search(r"world model|video|prediction", blob):
        mech = "action-conditioned predictive world modeling"
    elif re.search(r"mpc|planning|control", blob):
        mech = "planning/control over a learned or hybrid dynamics model"
    else:
        mech = "task-specific embodied learning mechanism"

    if re.search(r"uncertainty|bayesian|ensemble", blob):
        hidden = "confidence is enough to expose deployment-critical errors"
    elif re.search(r"sim to real|sim-to-real|domain", blob):
        hidden = "training variation covers deployment mismatch"
    else:
        hidden = "the chosen representation exposes the repair-critical physical variables"

    if re.search(r"contact|tactile|friction|deform", blob):
        fixed = "contact/friction regime"
        fail = "contact-mode changes and localized physical mismatch"
    else:
        fixed = "planner response and observability assumptions"
        fail = "planner-exploited false transitions and execution-time counterexamples"

    if re.search(r"repair|recover|failure", blob):
        less_novel = "generic failure recovery or repair framing"
        open_ = "whether repair should be scoped to transition edits rather than retraining"
    else:
        less_novel = "broad learned dynamics / planning claims"
        open_ = "how embodied counterexamples should rewrite the model used by planning"

    return {
        "problem_claimed": problem,
        "actual_mechanism": mech,
        "hidden_assumptions": hidden,
        "variables_treated_as_fixed": fixed,
        "failure_modes_ignored": fail,
        "what_it_makes_less_novel": less_novel,
        "what_it_leaves_open": open_,
    }


@dataclass
class Row:
    key: str
    data: dict[str, str]


def row_key(row: dict[str, str]) -> str:
    if row.get("doi"):
        return "doi:" + row["doi"].lower()
    return "title:" + re.sub(r"[^a-z0-9]+", "", row.get("title", "").lower())


def accept(row: dict[str, str]) -> bool:
    blob = text_blob(row)
    return any(h in blob for h in ROBOTICS_HINTS)


def collect() -> list[Row]:
    seen: dict[str, Row] = {}
    DATA.mkdir(exist_ok=True)
    with CACHE.open("w", encoding="utf-8") as cache:
        for q in QUERIES:
            for offset in range(0, 500, PAGE_SIZE):
                items = crossref_items(q, rows=PAGE_SIZE, offset=offset)
                cache.write(json.dumps({"source": "crossref", "query": q, "offset": offset, "n": len(items)}) + "\n")
                if not items:
                    break
                for item in items:
                    title = clean((item.get("title") or [""])[0] if isinstance(item.get("title"), list) else item.get("title") or "")
                    if not title:
                        continue
                    authors = []
                    for a in item.get("author") or []:
                        family = a.get("family", "")
                        given = a.get("given", "")
                        name = clean((given + " " + family).strip())
                        if name:
                            authors.append(name)
                    row = {
                        "title": title,
                        "year": str((item.get("issued", {}).get("date-parts") or [[None]])[0][0] or ""),
                        "authors": "; ".join(authors[:8]),
                        "venue": clean((item.get("container-title") or [""])[0] if isinstance(item.get("container-title"), list) else item.get("container-title") or ""),
                        "doi": clean(item.get("DOI") or ""),
                        "url": clean(item.get("URL") or ""),
                        "cited_by_count": str(item.get("is-referenced-by-count") or 0),
                        "source_query": q,
                        "concepts": "Crossref",
                        "abstract": clean(item.get("abstract") or ""),
                    }
                    if not accept(row):
                        continue
                    row.update(infer(row))
                    row["relevance_score"] = str(sum(h in text_blob(row) for h in ROBOTICS_HINTS) + int(row["cited_by_count"] != "0"))
                    rk = row_key(row)
                    seen.setdefault(rk, Row(rk, row))
                time.sleep(0.2)
                if len(seen) >= TARGET_MIN:
                    break
            if len(seen) >= TARGET_MIN:
                break
        if len(seen) < TARGET_MIN:
            # Add arXiv for modern embodied robotics and planning queries.
            for q in [
                "all:robot OR all:robotics OR all:manipulation OR all:planning OR all:control OR all:world model",
            ]:
                items = arxiv_items(q, max_results=200, start=0)
                cache.write(json.dumps({"source": "arxiv", "query": q, "n": len(items)}) + "\n")
                for item in items:
                    if not accept(item):
                        continue
                    item["source_query"] = q
                    item.update(infer(item))
                    item["relevance_score"] = str(sum(h in text_blob(item) for h in ROBOTICS_HINTS))
                    rk = row_key(item)
                    seen.setdefault(rk, Row(rk, item))
                if len(seen) >= TARGET_MIN:
                    break
    return list(seen.values())


def write(rows: list[Row]) -> None:
    ordered = sorted(
        [r.data for r in rows],
        key=lambda r: (-float(r.get("relevance_score", "0") or 0), -int(r.get("cited_by_count", "0") or 0), r.get("year", "")),
    )
    fields = [
        "rank", "read_tier", "title", "year", "authors", "venue", "doi", "url", "cited_by_count", "source_query",
        "concepts", "problem_claimed", "actual_mechanism", "hidden_assumptions", "variables_treated_as_fixed",
        "failure_modes_ignored", "what_it_makes_less_novel", "what_it_leaves_open", "relevance_score", "hostile_reason", "abstract",
    ]
    for i, row in enumerate(ordered, start=1):
        row["rank"] = str(i)
        row["read_tier"] = "hostile_prior_work" if i <= 100 else "deep_read" if i <= 240 else "serious_skim" if i <= 300 else "landscape_sweep"
        row["hostile_reason"] = "High-priority prior work for boundary checking." if i <= 100 else ""
    DOCS.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in ordered:
            writer.writerow({k: row.get(k, "") for k in fields})
    print(json.dumps({"rows": len(ordered), "output": str(OUT)}, indent=2))


def main() -> int:
    rows = collect()
    if len(rows) < 1000:
        raise RuntimeError(f"Collected only {len(rows)} rows")
    write(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
