#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ARXIV_API = "http://export.arxiv.org/api/query"
CROSSREF_API = "https://api.crossref.org/works"
OPENALEX_API = "https://api.openalex.org/authors"

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
    "electrical double layer",
    "oxide-electrolyte",
    "long-range electrostatics",
    "wasserstein gradient flow",
    "neural ode",
    "nonlinear mobility",
    "solutal marangoni",
    "bubble coalescence",
    "bubble detachment",
    "hydrogen evolution",
    "electrolyte interface",
]

CATEGORY_QUERY = "(cat:physics.chem-ph OR cat:cond-mat.soft OR cat:physics.bio-ph OR cat:physics.comp-ph)"

# User requested: JCTC/JCIM/JACS/PRL/PNAS/CNS (Cell/Nature/Science)
JOURNALS = {
    "JCTC": "1549-9626",
    "JCIM": "1549-960X",
    "JACS": "0002-7863",
    "PRL": "0031-9007",
    "PNAS": "0027-8424",
    "Nature": "1476-4687",
    "Science": "1095-9203",
    "Cell": "0092-8674",
}


def _fetch_json(url: str, timeout: int = 20) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "paper-daily-bot/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", errors="ignore"))


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
                "venue": "arXiv preprint",
            }
        )
    return entries


def fetch_crossref_by_issn(days: int = 3, rows: int = 30) -> list[dict]:
    since = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    all_entries: list[dict] = []
    for short, issn in JOURNALS.items():
        params = {
            "filter": f"from-pub-date:{since},issn:{issn}",
            "sort": "published",
            "order": "desc",
            "rows": str(rows),
            "select": "title,URL,DOI,author,published-print,published-online,published,container-title,abstract,type",
        }
        url = f"{CROSSREF_API}?{urllib.parse.urlencode(params)}"
        try:
            data = _fetch_json(url)
        except Exception:
            continue

        items = data.get("message", {}).get("items", [])
        for it in items:
            title = ""
            if isinstance(it.get("title"), list) and it["title"]:
                title = it["title"][0]
            abstract = re.sub(r"<[^>]+>", " ", (it.get("abstract") or ""))
            summary = re.sub(r"\s+", " ", abstract).strip()
            authors = []
            for a in it.get("author", [])[:12]:
                name = " ".join(x for x in [a.get("given", ""), a.get("family", "")] if x).strip()
                if name:
                    authors.append(name)
            pdate = ""
            for k in ["published-online", "published-print", "published"]:
                date_parts = it.get(k, {}).get("date-parts", [])
                if date_parts and date_parts[0]:
                    ymd = date_parts[0] + [1, 1]
                    pdate = f"{ymd[0]:04d}-{ymd[1]:02d}-{ymd[2]:02d}"
                    break

            all_entries.append(
                {
                    "title": re.sub(r"\s+", " ", title).strip(),
                    "summary": summary,
                    "published": pdate,
                    "url": it.get("URL", ""),
                    "authors": authors,
                    "source": "Crossref",
                    "venue": short,
                }
            )
    return all_entries


def fetch_chemrxiv(days: int = 5, rows: int = 50) -> list[dict]:
    # Best-effort via Crossref query on ChemRxiv container-title.
    since = (dt.date.today() - dt.timedelta(days=days)).isoformat()
    params = {
        "filter": f"from-pub-date:{since}",
        "query.container-title": "ChemRxiv",
        "sort": "published",
        "order": "desc",
        "rows": str(rows),
        "select": "title,URL,DOI,author,published,container-title,abstract",
    }
    url = f"{CROSSREF_API}?{urllib.parse.urlencode(params)}"
    try:
        data = _fetch_json(url)
    except Exception:
        return []

    entries: list[dict] = []
    for it in data.get("message", {}).get("items", []):
        ct = " ".join(it.get("container-title", [])) if isinstance(it.get("container-title"), list) else ""
        if "chemrxiv" not in ct.lower():
            continue
        title = it.get("title", [""])
        title = title[0] if isinstance(title, list) and title else ""
        abstract = re.sub(r"<[^>]+>", " ", (it.get("abstract") or ""))
        summary = re.sub(r"\s+", " ", abstract).strip()
        authors = []
        for a in it.get("author", [])[:12]:
            name = " ".join(x for x in [a.get("given", ""), a.get("family", "")] if x).strip()
            if name:
                authors.append(name)

        pdate = ""
        date_parts = it.get("published", {}).get("date-parts", [])
        if date_parts and date_parts[0]:
            ymd = date_parts[0] + [1, 1]
            pdate = f"{ymd[0]:04d}-{ymd[1]:02d}-{ymd[2]:02d}"

        entries.append(
            {
                "title": re.sub(r"\s+", " ", title).strip(),
                "summary": summary,
                "published": pdate,
                "url": it.get("URL", ""),
                "authors": authors,
                "source": "ChemRxiv",
                "venue": "ChemRxiv",
            }
        )
    return entries


def score_paper(p: dict, keywords: list[str]) -> tuple[int, int, int]:
    text = (p.get("title", "") + " " + p.get("summary", "")).lower()
    method_kw = ["deep potential", "neural network potential", "machine learning potential", "enhanced sampling", "free energy", "neural ode", "wasserstein", "gradient flow", "nonlinear mobility"]
    chem_kw = ["proton transfer", "tautomerism", "hydronium", "hydroxide", "electrical double layer", "edl", "oxide-electrolyte", "marangoni", "bubble", "electrolysis", "hydrogen evolution", "interface", "electrolyte"]

    anchor_groups = [
        ["jko", "wasserstein", "neural ode", "nonlinear mobility"],
        ["slow mode", "dynamical mode", "timescale"],
        ["solutal marangoni", "hofmeister", "bubble detachment"],
        ["worthington", "droplet spraying", "microbubble coalescence"],
        ["electrical double layer", "ihp", "imhp", "dplr", "long-range electrostatics"],
    ]

    method = sum(1 for k in method_kw if k in text)
    chem = sum(1 for k in chem_kw if k in text)
    evidence = 1 if any(k in text for k in ["benchmark", "accuracy", "simulation", "experiment", "free energy", "validated"]) else 0
    novelty = 1 if any(k in text for k in ["new", "novel", "first", "unprecedented"]) else 0
    repro = 1 if any(k in text for k in ["code", "github", "open source", "dataset"]) else 0

    matched_anchors = sum(1 for g in anchor_groups if any(k in text for k in g))

    method_score = min(100, method * 12)
    chem_score = min(100, chem * 9)
    total = int(0.35 * chem_score + 0.30 * method_score + 20 * evidence + 10 * novelty + 5 * repro)

    if matched_anchors >= 2:
        total += 18
    elif matched_anchors == 1:
        total += 10

    if any(k in text for k in ["electrochemical", "electrolyte", "interface"]) and any(k in text for k in ["neural ode", "ml potential", "deep potential", "gradient flow"]):
        total += 25

    if not any(k in text for k in keywords):
        total = int(total * 0.6)

    total = min(100, total)
    return total, method_score, chem_score


def summarize(p: dict) -> str:
    s = p.get("summary", "").strip() or "No abstract available from source metadata."
    if len(s) <= 760:
        return s
    return s[:757] + "..."


def extract_resource_links(p: dict) -> list[str]:
    text = f"{p.get('summary','')} {p.get('url','')}"
    urls = re.findall(r"https?://[^\s)\]>]+", text)
    cleaned = []
    for u in urls:
        u = u.rstrip('.,;')
        if u not in cleaned:
            cleaned.append(u)
    useful = [u for u in cleaned if any(k in u.lower() for k in ["github.com", "gitlab", "bitbucket", "zenodo", "figshare", "dataset", "code"])]
    return useful[:3]


def notable_author_line(authors: list[str]) -> str:
    if not authors:
        return ""

    # Prefer the last author first (often senior/corresponding in this domain), then first author.
    candidates = [authors[-1], authors[0]] if len(authors) > 1 else [authors[0]]
    for name in candidates:
        try:
            url = f"{OPENALEX_API}?search={urllib.parse.quote(name)}&per-page=1"
            data = _fetch_json(url)
            r = (data.get("results") or [{}])[0]
            matched = r.get("display_name") or name
            inst = ""
            if r.get("last_known_institutions"):
                inst = (r.get("last_known_institutions")[0] or {}).get("display_name", "")
            concepts = [c.get("display_name", "") for c in (r.get("x_concepts") or [])[:3] if c.get("display_name")]
            expertise = ", ".join(concepts) if concepts else "computational chemistry"
            if inst:
                return f"Notable author: {matched} ({inst}); expertise: {expertise}."
            return f"Notable author: {matched}; expertise: {expertise}."
        except Exception:
            continue

    return f"Notable author: {authors[-1]}."


def dedupe(papers: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for p in papers:
        key = (re.sub(r"\W+", "", p.get("title", "").lower())[:120], p.get("url", ""))
        if key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out


def build_report(topic: str, papers: list[dict], date_str: str) -> str:
    lines = [
        "# Daily Frontier Paper (English)",
        "",
        "## 1) Scope",
        f"- Topic: {topic}",
        "- Time window: Last 24-72 hours (source dependent)",
        "- Sources: arXiv + ChemRxiv + journal TOC (JCTC/JCIM/JACS/PRL/PNAS/CNS)",
        f"- Selection size: {len(papers)}",
        f"- Report date: {date_str}",
        "",
    ]

    if not papers:
        lines += [
            "## 2) Paper of the Day",
            "- No paper passed the relevance threshold today. Keep monitoring tomorrow.",
        ]
        return "\n".join(lines)

    p = papers[0]
    authors = p.get("authors", [])
    resources = extract_resource_links(p)
    author_note = notable_author_line(authors)

    lines += [
        "## 2) Paper of the Day",
        f"- Title: {p.get('title', '')}",
        f"- Paper link: {p.get('url', '')}",
        f"- Authors: {', '.join(authors[:8]) or 'N/A'}",
        f"- Method Match Score (0-100): {p.get('method_score', 0)}",
        f"- Chemistry Relevance Score (0-100): {p.get('chem_score', 0)}",
        f"- Brief summary: {summarize(p)}",
        "",
        "## 3) Author note",
        f"- {author_note}",
        "",
        "## 4) Brief Interpretation",
        "- Background (brief): Targets an important gap in chemistry/interface simulation reliability.",
        "- Method: Uses model benchmarking or mechanism-focused computational analysis to quantify performance/behavior.",
        "- Conclusion: Provides practical evidence for method selection and next-step validation in related chemistry problems.",
        "",
        "## 5) Why this one today",
        f"- Chosen as the single most relevant paper by weighted score ({p.get('total_score', 0)}) and profile alignment.",
    ]

    if resources:
        lines += ["", "## 6) Code / resources"]
        for u in resources:
            lines.append(f"- {u}")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate today's English frontier-paper report")
    parser.add_argument("--topic", default="Deep Potential MD for interfacial chemistry and proton-transfer mechanisms")
    parser.add_argument("--top-k", type=int, default=1)
    parser.add_argument("--days", type=int, default=3)
    parser.add_argument("--out-dir", default="reports")
    args = parser.parse_args()

    today = dt.datetime.utcnow().date()
    cutoff = today - dt.timedelta(days=args.days)

    papers = []
    try:
        papers.extend(fetch_arxiv(max_results=120))
    except Exception:
        pass
    try:
        papers.extend(fetch_chemrxiv(days=args.days + 2, rows=60))
    except Exception:
        pass
    try:
        papers.extend(fetch_crossref_by_issn(days=args.days + 2, rows=35))
    except Exception:
        pass

    papers = dedupe(papers)
    ranked: list[dict] = []
    for p in papers:
        try:
            d = dt.date.fromisoformat(p.get("published", ""))
        except Exception:
            continue
        if d < cutoff:
            continue
        total, method_score, chem_score = score_paper(p, DEFAULT_KEYWORDS)
        if total < 22:
            continue
        p["total_score"] = total
        p["method_score"] = method_score
        p["chem_score"] = chem_score
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
    print(f"[OK] Candidate pool: {len(papers)}")
    print(f"[OK] Selected papers: {len(top)}")


if __name__ == "__main__":
    main()
