# Eval results

Graded pairs: **6**. Judge: claude-sonnet-5 (blind, A/B order randomized).

## Head to head (same model, same prompt, with vs without the skill)

| Model | With skill wins | Without skill wins | Ties |
|---|---|---|---|
| haiku | 6 | 0 | 0 |

## Scores

*Usable as-is* and *invented facts* are the neutral measures. *Framework score* checks the skill's own criteria, so it naturally favors the skill.

| Model | Condition | Outputs | Usable as-is (1-5) | Framework score (1-5) | Invented facts (avg) | Followed request | Length OK |
|---|---|---|---|---|---|---|---|
| haiku | without-skill | 6 | 3.00 | 3.29 | 1.17 | 100% | 100% |
| haiku | with-skill | 6 | 4.17 | 4.34 | 0.50 | 100% | 100% |

## Per test

| Test | Model | Run | Winner | Judge's reason | Outputs |
|---|---|---|---|---|---|
| 01-hook-options | haiku | 1 | with-skill | B's hooks are more concrete and specific without presenting fabricated stats as fact—its one made-up dollar figure is explicitly flagged as an assumption to swap for real data, whereas A states two invented statistics ('8+ hours a week,' 'we asked 500 parents') as if true, which a copywriter would have to strip out before use. | [with](../evals/runs/01-hook-options/haiku/with-skill/run-1.md) / [without](../evals/runs/01-hook-options/haiku/without-skill/run-1.md) |
| 02-landing-page | haiku | 1 | with-skill | A delivers a tight, honest, conversational hero section with no fabricated credentials, while B fabricates a coach's track record and a social-proof stat that the requester never supplied, making it riskier to use as-is. | [with](../evals/runs/02-landing-page/haiku/with-skill/run-1.md) / [without](../evals/runs/02-landing-page/haiku/without-skill/run-1.md) |
| 03-cold-email | haiku | 1 | with-skill | B reads like a real, specific email from a person who understands a founder's world (runway, unit economics, ad spend) with a natural conversational flow and a low-pressure close, while A leans on bolded subheads and generic copywriter clichés that feel more like a template; B's edge does come with a couple of unverified specific numbers the founder should double-check before sending. | [with](../evals/runs/03-cold-email/haiku/with-skill/run-1.md) / [without](../evals/runs/03-cold-email/haiku/without-skill/run-1.md) |
| 04-cta-rewrite | haiku | 1 | with-skill | B leads with one concrete, ready-to-use rewrite backed by a tight 'why it works' breakdown, reads far more human, and still offers variants plus a clarifying question — whereas A is a bracket-heavy checklist of five templates that feels more like a copywriting lecture than a polished CTA. | [with](../evals/runs/04-cta-rewrite/haiku/with-skill/run-1.md) / [without](../evals/runs/04-cta-rewrite/haiku/without-skill/run-1.md) |
| 05-copy-critique | haiku | 1 | with-skill | B pinpoints the root cause more precisely — no defined avatar, which is why the promise, hook, and proof all feel generic — and cleanly separates that primary fix from secondary issues, ending with a concrete next question the requester can act on; A's advice is solid but blends the fix and the proof point together and stops short of a clear next step. | [with](../evals/runs/05-copy-critique/haiku/with-skill/run-1.md) / [without](../evals/runs/05-copy-critique/haiku/without-skill/run-1.md) |
| 06-offer-positioning | haiku | 1 | with-skill | Output A delivers a clean, usable framework and ad with no fabricated claims, clearly flagging where the client needs to supply real proof, while Output B's sample ad states a specific, unverified statistic ('47 sellers in 2025') and invented testimonial as if true, which a copywriter would have to strip out before it could ever run. | [with](../evals/runs/06-offer-positioning/haiku/with-skill/run-1.md) / [without](../evals/runs/06-offer-positioning/haiku/without-skill/run-1.md) |

## Notes

- SKILL.md version (sha256 prefix): `069b7b1b5917`
- Every output was generated with `claude -p` on a Claude Pro plan, from an empty folder, with user settings, skills, plugins, MCP servers, tools, and the Claude Code system prompt disabled. Without-skill system prompt: `You are a helpful assistant.` With-skill: the same line plus the full SKILL.md.
