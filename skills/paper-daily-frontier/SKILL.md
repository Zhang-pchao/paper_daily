---
name: paper-daily-frontier
description: Discover, filter, summarize, and report cutting-edge academic papers in English on a daily cadence. Use when users ask for literature scouting, research trend tracking, paper shortlists, daily/weekly paper digests, structured frontier-paper workflows with source selection/screening/report generation, or reliability operations for the related paper-daily automation pipeline (including OpenClaw gateway health checks and restart recommendations).
---

# Paper Daily Frontier Workflow

Run this workflow to produce a high-signal English daily paper digest.

## Inputs to collect

Collect or confirm:
- Topic focus (e.g., LLM agents, multimodal reasoning, diffusion models)
- Time window (default: last 24h)
- Source scope (arXiv, Papers With Code, top venues, Google Scholar)
- Output size (default: 5-10 papers)
- Audience (researcher, engineer, leadership)

If missing, infer conservative defaults and continue.

## Workflow

1. Build search queries from the topic and synonyms.
2. Gather candidate papers from allowed sources.
3. Deduplicate by DOI/arXiv ID/title normalization.
4. Screen papers with relevance + novelty + practical value.
5. Rank by impact signal (venue quality, novelty claim, methodology strength, reproducibility cues).
6. Generate concise summaries with:
   - What problem is solved
   - Core method/idea
   - Key results
   - Why it matters
   - Caveats
7. Produce the final digest using `references/report-template.md`.
8. If requested, generate a machine-readable dataset (JSON/CSV).

## Quality bar

Enforce:
- Evidence-first claims (no invented metrics)
- Clear uncertainty language when evidence is weak
- Distinguish paper claims vs your assessment
- Link every paper entry to its source URL

## Output rules

- Write in English.
- Prefer compact, high-information bullet points.
- Keep each paper summary within 120-180 words unless asked otherwise.
- End with 3-5 trend observations across the selected papers.

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
- Report template: `references/report-template.md`
- Gateway health guidance: `references/openclaw-gateway-health.md`
- Optional formatter script: `scripts/build_daily_digest.py`
- Optional gateway checker script: `scripts/check_gateway_health.sh`
