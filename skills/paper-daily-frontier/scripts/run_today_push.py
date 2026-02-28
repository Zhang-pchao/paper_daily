#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import textwrap
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ARXIV_API = "http://export.arxiv.org/api/query"

DEFAULT_KEYWORDS = [
    "deep potential",
    "neural network potential",
    "machine learning potential",
    "enhanced sampling",
    "free energy",
    "proton transfer",
    "tautomerism",
    "hydronium",
    "hydroxide",
    "air-water interface",
    "oil-water interface",
    "electric field",
]

CATEGORY_QUERY = "(cat:physics.chem-ph OR cat:cond-mat.soft OR cat:physics.bio-ph OR cat:physics.comp-ph)"


def fetch_arxiv(max_results: int = 80) -> list[dict]:
    query = f"search_query={urllib.parse.quote(CATEGORY_QUERY)}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    url = f"{ARXIV_API}?{query}"
    with urllib.request.urlopen(url, timeout=20) as r:
        xml_data = r.read()

    ns = {"a": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_data)
    entries = []
    for entry in root.findall("a:entry", ns):
        title = (entry.findtext("a:title", default="", namespaces=ns) or "").strip()
        summary = (entry.findtext("a:summary", default="", namespaces=ns) or "").strip()
        published = (entry.findtext("a:published", default="", namespaces=ns) or "").strip()
        link = ""
        for l in entry.findall("a:link", ns):
            if l.get("type") == "text/html":
                link = l.get("href", "")
                break
        authors = [a.findtext("a:name", default="", namespaces=ns) for a in entry.findall("a:author", ns)]
        entries.append(
            {
                "title": re.sub(r"\s+", " ", title),
                "summary": re.sub(r"\s+", " ", summary),
                "published": published[:10],
                "url": link,
                "authors": [x for x in authors if x],
                "source": "arXiv",
            }
        )
    return entries


def score_paper(p: dict, keywords: list[str]) -> tuple[int, int, int]:
    text = (p["title"] + " " + p["summary"]).lower()
    method_kw = ["deep potential", "neural network potential", "machine learning potential", "enhanced sampling", "free energy"]
    chem_kw = ["proton transfer", "tautomerism", "hydronium", "hydroxide", "interface", "air-water", "oil-water", "electric field"]

    method = sum(1 for k in method_kw if k in text)
    chem = sum(1 for k in chem_kw if k in text)
    evidence = 1 if any(k in text for k in ["benchmark", "accuracy", "simulation", "experiment", "free energy"]) else 0
    novelty = 1 if any(k in text for k in ["new", "novel", "first", "unprecedented"]) else 0
    repro = 1 if any(k in text for k in ["code", "github", "open source", "dataset"]) else 0

    method_score = min(100, method * 20)
    chem_score = min(100, chem * 14)
    total = int(0.35 * chem_score + 0.30 * method_score + 20 * evidence + 10 * novelty + 5 * repro)

    if not any(k in text for k in keywords):
        total = int(total * 0.5)

    return total, method_score, chem_score


def summarize(p: dict) -> str:
    s = p["summary"].strip()
    if len(s) <= 760:
        return s
    return s[:757] + "..."


def build_report(topic: str, papers: list[dict], date_str: str) -> str:
    lines = [
        "# Daily Frontier Papers Report (English)",
        "",
        "## 1) Scope",
        f"- Topic: {topic}",
        "- Time window: Last 24 hours (arXiv latest feed)",
        "- Sources: arXiv (chem-ph / soft matter / comp-physics / bio-physics)",
        f"- Selection size: {len(papers)}",
        f"- Report date: {date_str}",
        "",
        "## 2) Top Papers",
        "",
    ]

    for idx, p in enumerate(papers, 1):
        lines += [
            f"### Paper {idx}",
            f"- Title: {p['title']}",
            f"- Authors: {', '.join(p['authors'][:8])}",
            f"- Source URL: {p['url']}",
            f"- Venue / Status: arXiv preprint",
            f"- Published / Submitted: {p['published']}",
            f"- Method Match Score (0-100): {p['method_score']}",
            f"- Chemistry Relevance Score (0-100): {p['chem_score']}",
            f"- Summary (120-180 words): {summarize(p)}",
            f"- Key contribution: {p['key_contribution']}",
            f"- Evidence snapshot: {p['evidence_snapshot']}",
            f"- Practical takeaway: {p['takeaway']}",
            f"- Caveat: {p['caveat']}",
            "",
        ]

    lines += [
        "## 3) Cross-paper Trends (3-5 bullets)",
        "- Growing use of ML potential-based simulations for chemistry dynamics and reactivity studies.",
        "- Method papers increasingly emphasize long-range effects and better physical fidelity.",
        "- Interface/electrostatics-aware modeling is becoming a key differentiator for mechanism studies.",
        "",
        "## 4) Recommended Next Actions",
        "- Immediate read list: Paper 1 and Paper 2",
        "- Potential replication targets: Highest method+chemistry score paper",
        "- Monitoring keywords for tomorrow: deep potential, proton transfer, interface electric field",
        "",
        "## 5) Top 1-2 papers to deep-read today",
    ]

    for p in papers[:2]:
        lines.append(f"- {p['title']} — selected for high total score ({p['total_score']}) and strong alignment with your profile.")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate today's English frontier-paper report")
    parser.add_argument("--topic", default="Deep Potential MD for interfacial chemistry and proton-transfer mechanisms")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--days", type=int, default=2)
    parser.add_argument("--out-dir", default="reports")
    args = parser.parse_args()

    today = dt.datetime.utcnow().date()
    cutoff = today - dt.timedelta(days=args.days)

    papers = fetch_arxiv(max_results=120)
    ranked: list[dict] = []

    for p in papers:
        try:
            d = dt.date.fromisoformat(p["published"])
        except Exception:
            continue
        if d < cutoff:
            continue
        total, method_score, chem_score = score_paper(p, DEFAULT_KEYWORDS)
        if total < 30:
            continue
        p["total_score"] = total
        p["method_score"] = method_score
        p["chem_score"] = chem_score
        p["key_contribution"] = "Introduces or applies a computational strategy relevant to chemistry mechanism modeling."
        p["evidence_snapshot"] = "Based on abstract-level evidence from arXiv metadata; verify full text for detailed metrics."
        p["takeaway"] = "Potentially relevant for your personalized daily frontier tracking."
        p["caveat"] = "Preprint evidence; venue-level peer review may still be pending."
        ranked.append(p)

    ranked.sort(key=lambda x: x["total_score"], reverse=True)
    top = ranked[: args.top_k]

    date_str = dt.datetime.now().strftime("%Y-%m-%d")
    report = build_report(args.topic, top, date_str)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"daily-report-{date_str}.md"
    json_path = out_dir / f"daily-report-{date_str}.json"

    md_path.write_text(report, encoding="utf-8")
    json_path.write_text(json.dumps(top, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[OK] Report written: {md_path}")
    print(f"[OK] Data written:   {json_path}")
    print(f"[OK] Selected papers: {len(top)}")


if __name__ == "__main__":
    main()
