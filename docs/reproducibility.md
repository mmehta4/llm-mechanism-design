# Reproducibility notes

## What we pin

- **Exact model version strings** (`config.MODELS[...].api_id`), written into every
  logged row. Providers deprecate and silently update models; a result that cannot
  name its subject cannot be rechecked.
- **Random seeds** for all private-value draws (`config.MASTER_SEED`), so the same
  sequence of game parameters regenerates exactly.
- **Effort level**, logged per trial.
- **Full raw transcripts**, not just parsed actions — the audit trail, and in
  practice the most interesting qualitative material in the project.

## What we cannot pin — and why it matters

**Sampling temperature is not available on the current Anthropic models.**
`temperature`, `top_p`, and `top_k` were removed on Opus 5, Sonnet 5, and the
4.7/4.8 family; passing any of them returns HTTP 400. Haiku 4.5 and older models
still accept them.

Consequences for the experimental design:

1. **Responses are not deterministic and cannot be made so.** This is fine — the
   project measures *distributions* of behaviour, not single actions, so
   stochasticity is the object of study rather than a nuisance. But it must be
   stated plainly in the writeup rather than glossed.
2. **Do not report a temperature setting you did not actually control.** Reviewers
   in this area know the current API surface.
3. **Cross-model comparison is confounded slightly** by the fact that arms differ
   in whether sampling was pinnable at all. Note it in limitations.

**Reasoning depth is ordinal, not binary.** The overview lists "chain-of-thought
allowed vs. not" as a condition. Thinking is adaptive and on by default on current
models, so a clean on/off contrast is not available. Use `output_config.effort`
(`low` → `max`) instead. This is a better factor anyway: it is ordinal, giving a
dose-response curve rather than a two-point contrast.
