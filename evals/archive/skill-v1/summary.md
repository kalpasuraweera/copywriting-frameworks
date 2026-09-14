# Eval results

Graded pairs: **10**. Judge: claude-sonnet-5 (blind, A/B order randomized).

## Head to head (same model, same prompt, with vs without the skill)

| Model | With skill wins | Without skill wins | Ties |
|---|---|---|---|
| haiku | 5 | 1 | 0 |
| sonnet | 1 | 3 | 0 |

## Scores

*Usable as-is* and *invented facts* are the neutral measures. *Framework score* checks the skill's own criteria, so it naturally favors the skill.

| Model | Condition | Outputs | Usable as-is (1-5) | Framework score (1-5) | Invented facts (avg) | Followed request | Length OK |
|---|---|---|---|---|---|---|---|
| haiku | without-skill | 6 | 2.83 | 3.36 | 1.00 | 100% | 100% |
| haiku | with-skill | 6 | 3.50 | 4.19 | 0.33 | 83% | 83% |
| sonnet | without-skill | 4 | 3.50 | 3.82 | 1.00 | 100% | 100% |
| sonnet | with-skill | 4 | 3.00 | 3.69 | 0.50 | 75% | 75% |

## Per test

| Test | Model | Run | Winner | Judge's reason | Outputs |
|---|---|---|---|---|---|
| 01-hook-options | haiku | 1 | with-skill | B delivers tighter, more Twitter-native hooks with a clearer defined avatar, and it flags its one data-based hook as conditional rather than presenting fabricated stats as fact the way A does with its invented '416 hours a year' and '500 parents surveyed' claims. | [with](runs/01-hook-options/haiku/with-skill/run-1.md) / [without](runs/01-hook-options/haiku/without-skill/run-1.md) |
| 01-hook-options | sonnet | 1 | without-skill | A delivers five punchy, ready-to-tweet hooks with a natural voice and minimal extra clutter, while B's hooks are solid but buried under rubric-style annotations that would need stripping before posting, making A the more immediately usable deliverable despite both containing a few unverified stats. | [with](runs/01-hook-options/sonnet/with-skill/run-1.md) / [without](runs/01-hook-options/sonnet/without-skill/run-1.md) |
| 02-landing-page | haiku | 1 | with-skill | A delivers a sharper, more specific avatar and hook without fabricating any credibility claims, honestly flagging where proof needs to be added; B invents a specific coach credential and a '5,000+ marathoners' stat presented as fact, which the requester would have to strip or fact-check before using. | [with](runs/02-landing-page/haiku/with-skill/run-1.md) / [without](runs/02-landing-page/haiku/without-skill/run-1.md) |
| 02-landing-page | sonnet | 1 | without-skill | A delivers exactly what was asked—a clean, ready-to-use hero section for the stated beginner audience—while B second-guesses the brief, silently swaps the target avatar from 'beginner' to 'experienced runner,' and buries the actual copy inside a lot of unrequested meta-commentary and a framework breakdown, making it far less usable as a direct handoff. | [with](runs/02-landing-page/sonnet/with-skill/run-1.md) / [without](runs/02-landing-page/sonnet/without-skill/run-1.md) |
| 03-cold-email | haiku | 1 | without-skill | A delivers exactly what was asked—a single, ready-to-send cold email with a clear structure and CTA—while B buries a solid email inside a much longer strategy document (personas, hook-scoring, rationale) that the requester didn't ask for and would have to dig through and heavily customize before use. | [with](runs/03-cold-email/haiku/with-skill/run-1.md) / [without](runs/03-cold-email/haiku/without-skill/run-1.md) |
| 03-cold-email | sonnet | 1 | with-skill | A's email reads cleanly with no grammatical errors, keeps a single disciplined CTA (and explicitly warns against diluting it), and pairs the draft with a sharper strategic breakdown, while B's opening line contains an awkward, broken sentence and stacks two asks (free teardown + call) that muddy the CTA. | [with](runs/03-cold-email/sonnet/with-skill/run-1.md) / [without](runs/03-cold-email/sonnet/without-skill/run-1.md) |
| 04-cta-rewrite | haiku | 1 | with-skill | B diagnoses the CTA's flaws more precisely (Who/What/When/How), delivers one fully ready-to-use rewrite alongside contextual options, and reads like an actual copywriter's voice rather than A's generic checklist-and-emoji listicle. | [with](runs/04-cta-rewrite/haiku/with-skill/run-1.md) / [without](runs/04-cta-rewrite/haiku/without-skill/run-1.md) |
| 04-cta-rewrite | sonnet | 1 | without-skill | B delivers more ready-to-use, varied CTA options with tighter copy and a clear explanation of principles, while A spends more space on diagnostic framework than actual usable rewrites. | [with](runs/04-cta-rewrite/sonnet/with-skill/run-1.md) / [without](runs/04-cta-rewrite/sonnet/without-skill/run-1.md) |
| 05-copy-critique | haiku | 1 | with-skill | B nails the single root cause ('no promise') and shows the diagnostic 'so what?' test that ties audience, proof, urgency, and differentiation back to it, giving the requester a reusable way to think about the fix, whereas A's diagnosis ('vague benefits') is accurate but more generic and less unifying. | [with](runs/05-copy-critique/haiku/with-skill/run-1.md) / [without](runs/05-copy-critique/haiku/without-skill/run-1.md) |
| 06-offer-positioning | haiku | 1 | with-skill | A is just as sharp and punchy as B but is honest about what it doesn't know (flagging proof as '???' and asking for real results), while B fabricates a specific statistic ('47 Shopify/Amazon sellers in 2025') directly in the ad copy, which is a false claim the business owner couldn't actually run without lying to prospects. | [with](runs/06-offer-positioning/haiku/with-skill/run-1.md) / [without](runs/06-offer-positioning/haiku/without-skill/run-1.md) |

## Notes

- SKILL.md version (sha256 prefix): `1a370faf3452`
- Every output was generated with `claude -p` on a Claude Pro plan, from an empty folder, with user settings, skills, plugins, MCP servers, tools, and the Claude Code system prompt disabled. Without-skill system prompt: `You are a helpful assistant.` With-skill: the same line plus the full SKILL.md.
