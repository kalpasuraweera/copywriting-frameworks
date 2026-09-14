# Archive: skill v1 results

These are the results from the first version of `SKILL.md` (sha256 prefix `1a370faf3452`, commit `f45c929`). They're kept so the iteration is visible, not hidden.

## What's here

- **Haiku 4.5:** all 6 tests, with and without the skill, blind-judged by Sonnet 5. With skill won 5 of 6.
- **Sonnet 5:** a partial, unplanned run. Tests 01–04 were fully run and judged before the run was stopped. Test 06 only has one condition, so it wasn't judged. With skill won 1 of 4.

See [`summary.md`](summary.md) for scores and the judge's reasons.

## What we learned, and what changed in v2

Every with-skill loss traced back to the skill's instructions, not the frameworks:

1. **Framework reasoning around the copy.** v1 told the model to "briefly show your thinking before the draft." Both models turned that into Six P's breakdowns, hook-score annotations, and notes wrapped around the deliverable. The judge marked these outputs as less usable, or as not following the request (Haiku 03, Sonnet 01, Sonnet 04).
2. **Changing the brief.** The v1 "sanity-check the offer" rule led Sonnet to switch the landing page's audience from beginners to experienced runners (Sonnet 02).
3. **Templates instead of copy.** With missing context, the model returned fill-in-the-blank templates and questions instead of finished copy (Sonnet 04).
4. **Invented details slipped through.** Examples: made-up capacity scarcity (Haiku 06) and a sample case study with numbers (Haiku 03).

v2 puts the deliverable first, keeps the brief's audience, asks for finished copy built on sensible assumptions, and extends the no-invention rule to scarcity and "example" stats. Without-skill outputs don't depend on the skill, so the Haiku without-skill runs were reused for v2. Only the with-skill runs were regenerated.

Note: v2 was tuned using these same 6 prompts, so part of its improvement could be overfitting to them.
