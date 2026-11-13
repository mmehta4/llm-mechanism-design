# Deviations and run notes: pre-registration addendum (osf.io/ujvpx)

Registered on OSF on 13 November 2026 at osf.io/ujvpx (public, no embargo). The attached file's
SHA-256 is `74912ffd…160ac`, which matches the lock in `experiments/addendum.py` (commit
0baf39a). Collection started after registration, at about 01:42 on 13 November 2026 (local time).

1. **Mistral Large 4 split into four shards.** It averaged about 250 s per question, about 14
   per hour. About ten minutes into the run, its single process was stopped and restarted as
   four shards (`--shard i/4`):
   - the shards are disjoint, and together they are exactly the registered plan;
   - writes to the answer file are file-locked, as in Stages 2B–5.

   One request was in flight when the single process stopped, and its answer was never recorded.
   That question is asked again by its shard, exactly as a server failure would be. No recorded
   answer is discarded or replaced.

2. **gpt-oss and Gemini split across the study's existing keys (13 November, about 12:20).**
   Both reached their free-tier daily quotas:
   - Gemini after 231 questions;
   - gpt-oss after 188 questions.

   Their single processes were idle at the time, waiting for the quotas to reset, so no request
   was in flight. They were restarted as shards on the keys already approved for this study in
   deviation 12 of the main record (`docs/deviations-from-preregistration.md`), where the providers
   confirmed in writing that this is permitted:
   - gpt-oss: four shards on Groq keys 1–4;
   - Gemini: two shards on Gemini keys 1–2.

   The models, providers and settings are unchanged. The shards are disjoint, together they are
   the registered plan, and answers already recorded are kept.

3. **Two shards moved to a second key (13 November, about 13:45).** The first shards of gpt-oss
   (Groq key 1) and Gemini (Gemini key 1) reached their keys' daily quotas, while the other
   shards had finished. Both were idle, waiting for the quota to reset, with no request in flight.
   They were restarted, unchanged (`--shard 1/4` and `--shard 1/2`), on Groq key 2 and Gemini key
   2 respectively, which are keys already approved for this study (note 2). Nothing else changed.

4. **Pause while the computer slept.** No answers were recorded between about 03:15 and 12:20
   on 13 November (local time), because the computer running the collection slept. The runs
   resumed where they stopped. A pause changes only when answers are collected, not which
   questions are asked, and every arm is still collected in the same shuffled order.
