#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    p = argparse.ArgumentParser(description="Add a PDF paper anchor into category library")
    p.add_argument("--title", required=True)
    p.add_argument("--year", type=int, default=0)
    p.add_argument("--category", required=True, help="Category id, e.g. proton-transfer-tautomerism")
    p.add_argument("--library", default="skills/paper-daily-frontier/references/pdf-library-zhang-pchao.json")
    args = p.parse_args()

    path = Path(args.library)
    data = json.loads(path.read_text(encoding="utf-8"))

    papers = data.setdefault("papers", [])
    exists = any((x.get("title", "").strip().lower() == args.title.strip().lower()) for x in papers)
    if exists:
        print("[SKIP] Paper already exists")
        return

    papers.append({"title": args.title, "year": args.year, "category": args.category})
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] Added: {args.title} -> {args.category}")


if __name__ == "__main__":
    main()
