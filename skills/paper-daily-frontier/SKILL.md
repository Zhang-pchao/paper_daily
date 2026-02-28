---
name: paper-daily-frontier
description: Discover, filter, summarize, and report cutting-edge academic papers in English on a daily cadence. Use when users ask for literature scouting, research trend tracking, paper shortlists, daily/weekly paper digests, structured frontier-paper workflows with source selection/screening/report generation, or reliability operations for the related paper-daily automation pipeline (including OpenClaw gateway health checks and restart recommendations).
---

# Paper Daily Frontier Workflow

Run this workflow to produce a high-signal English daily paper digest.

## Inputs to collect

Collect or confirm:
- Topic focus
- Time window (default: last 24h)
- Source scope
- Output size (default: 1 paper)
- Audience (researcher, engineer, leadership)

If missing, infer defaults from `references/profile-zhang-pchao.md` and continue.

## Workflow

1. Load default field profile from `references/profile-zhang-pchao.md`.
2. Load anchor papers from `references/paper-anchors-2026-02.md` and apply anchor-aware relevance boost.
3. Build search queries from profile keywords and topic synonyms.
3. Gather candidate papers from preferred sources.
4. Deduplicate by DOI/arXiv ID/title normalization.
5. Screen papers with relevance + novelty + practical value.
6. Rank with profile-weighted scoring (method match + chemistry relevance + evidence quality).
7. Generate concise summaries with:
   - What problem is solved
   - Core method/idea
   - Key results
   - Why it matters
   - Caveats
8. Produce the final digest using `references/report-template.md`.
9. Keep only the single highest-ranked paper as "Paper of the Day".
10. Add a brief interpretation section with:
   - Research background (why this question matters)
   - Method (how the paper studies the problem)
   - Conclusion (main findings and implications)
11. If requested, generate a machine-readable dataset (JSON/CSV).

## Command trigger

When user says **"今日推送"** or **"再来一篇"**, run:

```bash
bash skills/paper-daily-frontier/scripts/today_push.sh
```

Category push is also supported, for example:

```bash
bash skills/paper-daily-frontier/scripts/today_push.sh --category bubble-marangoni-electrolysis
```

The script keeps same-day history (per category) and skips already-pushed papers by default.
For `slow-modes-statistical-dynamics`, enforce domain guardrails: keep chemistry/electrochemistry/fluid-dynamics papers and reject astronomy/cosmology content.
Then return `reports/daily-report-YYYY-MM-DD.md` as the English daily digest output (single-paper mode by default).

## Quality bar

Enforce:
- Evidence-first claims (no invented metrics)
- Clear uncertainty language when evidence is weak
- Distinguish paper claims vs your assessment
- Link every paper entry to its source URL

## Output rules

- Write in English.
- Prefer compact, high-information bullet points.
- Omit issue/volume metadata (journal bibliographic details) unless explicitly requested.
- Keep one clean primary link to the paper.
- Add one short but concrete "Notable author" line with institution + specialty + known method direction (search-based, not generic).
- If code/data is available, add explicit resource links (GitHub/project/dataset).
- If no code/data link is found, omit the entire code/resources section.
- Keep interpretation concise and method-first: brief background, then focus on method and conclusion.

## Reliability operations (optional)

Use this section when the paper-daily pipeline depends on an OpenClaw gateway runtime.

1. Run a gateway health check using `openclaw gateway status`.
2. Classify status:
   - Healthy: process running, API responding, no repeated crash loop
   - Degraded: slow response, intermittent failures, repeated reconnects
   - Down: process stopped or unresponsive
3. For Degraded or Down states, provide restart recommendation in this order:
   - `openclaw gateway restart` (preferred)
   - If still failing: `openclaw gateway stop` then `openclaw gateway start`
4. After restart, re-check status and report final state.
5. Include a short incident note in the daily report if availability impacted output.

Never claim a restart solved the issue unless post-restart status confirms recovery.

## Resources

- Source guidance: `references/sources.md`
- Personalized profile defaults: `references/profile-zhang-pchao.md`
- Paper anchors: `references/paper-anchors-2026-02.md`
- PDF category library: `references/pdf-library-zhang-pchao.json`
- Report template: `references/report-template.md`
- Gateway health guidance: `references/openclaw-gateway-health.md`
- Optional formatter script: `scripts/build_daily_digest.py`
- Auto daily-push script: `scripts/run_today_push.py`
- Trigger wrapper: `scripts/today_push.sh`
- Optional gateway checker script: `scripts/check_gateway_health.sh`
