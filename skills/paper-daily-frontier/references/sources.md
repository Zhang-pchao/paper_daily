# Sources and Screening Reference

## Priority source mix

1. arXiv (recent submissions in chem-ph / soft-matter / comp-physics / bio-physics)
2. ChemRxiv (chemistry preprints)
3. Journal TOC / metadata streams (JCTC, JCIM, JACS, PRL, PNAS, Cell, Nature, Science, Nature Chemistry, Nature Communications)
4. Google Scholar (citation tracking and related expansion)

## Suggested query pattern

Use combinations of:
- Chemistry problem term (EDL, proton transfer, bubble dynamics, electrolysis)
- Method term (ML potential, enhanced sampling, neural ODE, gradient flow)
- Interface/electrochem term (oxide-electrolyte, HER, Marangoni)

Example:
- "machine learning potential" AND "electrical double layer" AND oxide-electrolyte
- "hydrogen evolution" AND "solutal Marangoni" AND bubble detachment
- "Wasserstein gradient flow" AND "nonlinear mobility" AND particle method

## Screening rubric (1-5)

- Relevance to target chemistry/interface problem
- Method overlap with user profile and anchors
- Evidence quality (clear metrics, validation, mechanistic support)
- Practical applicability for user’s workflow
- Reproducibility signals (code/data/supplemental methods)

Weighted score:
`0.35 chemistry + 0.30 method + 0.20 evidence + 0.10 novelty + 0.05 reproducibility`

## Exclusion signals

- Weak relation to chemistry/interface/electrochem focus
- Purely generic method paper with no mechanistic tie-in
- Duplicate updates with no substantive new contribution
