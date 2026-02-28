#!/usr/bin/env python3
"""Build a markdown digest from a JSON list of papers.

Input JSON schema (list):
[
  {
    "title": "...",
    "authors": ["A", "B"],
    "url": "https://...",
    "venue": "arXiv",
    "date": "2026-02-28",
    "summary": "...",
    "contribution": "...",
    "evidence": "...",
    "takeaway": "...",
    "caveat": "..."
  }
]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def format_paper(i: int, p: dict) -> str:
    authors = p.get("authors", [])
    if isinstance(authors, list):
        authors = ", ".join(authors)

    return f"""### Paper {i}
- Title: {p.get('title', 'N/A')}
- Authors: {authors or 'N/A'}
- Source URL: {p.get('url', 'N/A')}
- Venue / Status: {p.get('venue', 'N/A')}
- Published / Submitted: {p.get('date', 'N/A')}
- Summary: {p.get('summary', 'N/A')}
- Key contribution: {p.get('contribution', 'N/A')}
- Evidence snapshot: {p.get('evidence', 'N/A')}
- Practical takeaway: {p.get('takeaway', 'N/A')}
- Caveat: {p.get('caveat', 'N/A')}
"""


def build(topic: str, window: str, sources: str, papers: list[dict]) -> str:
    header = f"""# Daily Frontier Papers Report (English)

## 1) Scope
- Topic: {topic}
- Time window: {window}
- Sources: {sources}
- Selection size: {len(papers)}

## 2) Top Papers

"""
    body = "\n".join(format_paper(i + 1, p) for i, p in enumerate(papers))
    footer = """
## 3) Cross-paper Trends (3-5 bullets)
- 
- 
- 

## 4) Recommended Next Actions
- Immediate read list:
- Potential replication targets:
- Monitoring keywords for tomorrow:
"""
    return header + body + "\n" + footer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input JSON")
    parser.add_argument("--output", required=True, help="Path to output markdown")
    parser.add_argument("--topic", default="Unspecified topic")
    parser.add_argument("--window", default="Last 24 hours")
    parser.add_argument("--sources", default="arXiv, Papers With Code")
    args = parser.parse_args()

    papers = json.loads(Path(args.input).read_text(encoding="utf-8"))
    if not isinstance(papers, list):
        raise ValueError("Input JSON must be a list of paper objects")

    markdown = build(args.topic, args.window, args.sources, papers)
    Path(args.output).write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
