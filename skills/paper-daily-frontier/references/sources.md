# Sources and Screening Reference

## Priority source mix

1. arXiv (recent submissions in relevant categories)
2. ChemRxiv (chemistry preprints)
3. Journal TOC / metadata streams (JCTC, JCIM, JACS, PRL, PNAS, Cell, Nature, Science)
4. Papers With Code (new papers + benchmarks)
5. Google Scholar (for citation and related-work expansion)

## Suggested query pattern

Use combinations of:
- Core topic term
- Method family
- Task/application term
- Constraint term (efficiency, robustness, alignment, etc.)

Example:
- "LLM agent planning tool use benchmark"
- "multimodal reasoning synthetic data distillation"

## Screening rubric (1-5)

- Relevance to target topic
- Novelty of method
- Empirical strength
- Practical applicability
- Reproducibility signals (code/data/ablations)

Compute weighted score if needed:
`0.30 relevance + 0.25 novelty + 0.20 empirical + 0.15 applicability + 0.10 reproducibility`

## Exclusion signals

- Duplicate preprint with no meaningful revision
- Weak evidence for major claims
- Pure marketing language with limited technical substance
