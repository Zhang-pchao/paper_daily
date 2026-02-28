# Personalized Research Push Profile (Zhang-pchao)

## Core field positioning

- Main track: Computational/Theoretical Chemistry for electrochemical and interfacial systems
- Method backbone: Deep Potential / ML potentials, enhanced sampling, gradient-flow-inspired modeling
- Problem focus:
  1. Water/electrolyte interfaces and EDL microstructure under pH/electric-field effects
  2. Proton transfer / tautomerism / reactive events in solvated environments
  3. Bubble dynamics in electrolysis (coalescence, Marangoni, detachment)
  4. High-dimensional transport/dynamics methods linked to chemistry mechanisms

## Priority sources

Tier A (must-have):
- ChemRxiv
- Journal TOC: JCTC, JCIM, JACS, Langmuir, PRL, PNAS, Nature, Science
- Nature-family expansion: Nature Communications, Nature Chemistry, Nature Physics, Nature Computational Science, Nature Materials, Nature Catalysis, Nature Energy
- Other high-impact expansion: Science Advances, Joule, Energy & Environmental Science, ACS Energy Letters, Angewandte, Chemical Science, JPCL

Tier B (method expansion):
- arXiv: physics.chem-ph, cond-mat.soft, physics.bio-ph, physics.comp-ph

Tier C (supplement):
- Google Scholar alerts (keyword + author)

## Default keyword pack (English)

- deep potential molecular dynamics
- machine learning potential
- long-range electrostatics
- enhanced sampling
- Wasserstein gradient flow
- neural ODE
- nonlinear mobility
- electrical double layer
- oxide-electrolyte interface
- proton transfer
- tautomerism
- solutal Marangoni
- bubble coalescence
- bubble detachment
- electrolysis hydrogen evolution

## Query templates

1. ("deep potential" OR "machine learning potential") AND ("electrical double layer" OR "oxide-electrolyte")
2. ("neural ODE" OR "Wasserstein" OR "gradient flow") AND ("nonlinear mobility" OR "particle method")
3. ("hydrogen evolution" OR HER) AND ("solutal Marangoni" OR "bubble coalescence" OR "bubble detachment")
4. ("proton transfer" OR tautomerism) AND ("enhanced sampling" OR "free energy") AND interface

## Ranking preference

Use total score (0-100):
- 35% chemistry relevance
- 30% method match
- 20% evidence quality
- 10% novelty signal
- 5% reproducibility signal

Venue-priority bonus (same relevance情况下优先高影响期刊):
- Tier S: Nature / Science / Cell / JACS (+10~12)
- Tier A: Nature Chemistry / Nature Communications / Nature Catalysis / Nature Energy / PNAS / PRL (+8~11)
- Tier B: JCTC / JCIM / JPCL / Joule / EES / Chemical Science / Angewandte (+7~9)

Anchor-aware bonus (from `references/paper-anchors-2026-02.md`):
- +10 if strong overlap with one anchor
- +18 if overlap with two or more anchors
- +25 if method novelty + electrochemical-interface relevance both present

## Output preference

- Daily report language: English
- Daily shortlist size: 1 paper (only the most relevant one)
- Include a brief interpretation: background (very short), method (main), conclusion (main)
- Use only essential metadata: title + paper link
- Add one-line notable-author context with institution + expertise + known method direction
- Add code/resource links only when available; otherwise omit this block
