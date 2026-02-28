# paper_daily

Repository for an English-first academic frontier paper workflow skill.

## Current scaffold

- `skills/paper-daily-frontier/SKILL.md` – main skill instructions
- `skills/paper-daily-frontier/references/sources.md` – source and screening rubric
- `skills/paper-daily-frontier/references/profile-zhang-pchao.md` – personalized profile defaults
- `skills/paper-daily-frontier/references/paper-anchors-2026-02.md` – user-provided paper anchors for relevance boosting
- `skills/paper-daily-frontier/references/report-template.md` – English daily report template
- `skills/paper-daily-frontier/scripts/run_today_push.py` – auto-fetch + ranking + report generator
- `skills/paper-daily-frontier/scripts/today_push.sh` – command trigger wrapper for "今日推送" / "再来一篇" (same-day dedup, per category)
- `skills/paper-daily-frontier/scripts/add_pdf_to_library.py` – add new PDF anchors into existing/new categories
- `skills/paper-daily-frontier/references/pdf-library-zhang-pchao.json` – category definitions + paper catalog
- `skills/paper-daily-frontier/scripts/build_daily_digest.py` – optional JSON→Markdown digest formatter

## Next steps

1. Connect real source ingestion (arXiv / PWC / venue feeds).
2. Add ranking automation and dedup logic.
3. Add scheduled daily run and automatic report delivery.
