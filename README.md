# Copywriting Frameworks for Claude

**Get marketing copy from Claude you can actually ship: written for a real reader, in a human voice, without made-up stats.**

A free skill for Claude Code, Claude.ai, and other AI agents, built from Jay Yang's copywriting course. It was blind-tested, and every raw output is published.

## Install

Using Claude Code? Run these two commands and it's ready in your next session:

```
/plugin marketplace add kalpasuraweera/copywriting-frameworks
/plugin install copywriting-frameworks@kalpasuraweera
```

<details>
<summary>Other ways to install: Claude.ai, Cursor/Codex and other agents, or manual</summary>

**Claude.ai / Claude apps**
Download [`copywriting-frameworks.skill`](https://github.com/kalpasuraweera/copywriting-frameworks/releases/latest/download/copywriting-frameworks.skill) from the [latest release](https://github.com/kalpasuraweera/copywriting-frameworks/releases/latest) and upload it via **Settings → Skills**.

**Any coding agent (Claude Code, Cursor, Codex, and more)**
```bash
npx skills add kalpasuraweera/copywriting-frameworks
```
Add `-g` to install it for all your projects.

**Manual**
```bash
git clone https://github.com/kalpasuraweera/copywriting-frameworks
cp -r copywriting-frameworks/skills/copywriting-frameworks ~/.claude/skills/
```

**Updating (Claude Code plugin):** `/plugin marketplace update kalpasuraweera`
</details>

## The problem

Ask an AI for a Twitter hook about a meal-kit brand and you'll get something like this:

> "Busy parents spend an avg of 8+ hours a week on meal planning & grocery shopping. That's 416 hours a year you're NOT with your family."

It sounds convincing. But nobody gave it that number. So before you can post it, you fact-check every line. And most of the time, you end up rewriting it.

## What changes with the skill

Same model, same prompts. The only difference is the skill:

| The request | Without the skill | With the skill |
|---|---|---|
| A hook for a meal-kit brand | "Busy parents spend an avg of 8+ hours a week on meal planning…" *(invented stat)* | "You know that guilt? Ordering takeout for the third time this week because you 'don't have time to cook'? We figured out how to stop it." |
| A landing page for a marathon plan | "…a certified coach who's trained 5,000+ first-time marathoners" *(invented credential)* | "Finish strong and uninjured — without 16 weeks of training." |
| Fix "Feel free to reach out anytime" | "Get a free [specific offer] — book your [call/demo/consultation] now" | "Schedule your free strategy call this week. [Schedule now →]" |

*Quotes are verbatim from the test outputs in [`examples/`](examples/).*

## How it works

Most AI copy starts writing straight away. That's why it sounds generic and fills gaps with invented proof. This skill makes Claude think like a copywriter first, then write:

| Step | What Claude does | Key ideas |
|------|------------------|-----------|
| **1. Think — Six P's** | Works out the strategy before any words | **People** (one specific reader) · **Positioning** (why you over alternatives) · **Promise** (an outcome, found with the "so what?" test) · **Proof** (real, and relatable to the reader) · **Priority** (an honest reason to act now) · **Process** (how it works, in one line) |
| **2. Write — Five C's** | Sets the voice | Clear · Concise · Concrete · Conversational · Cadence |
| **3. Structure** | Shapes the piece | A hook scored on benefit × relevance × credibility ÷ effort · a body with *What/Why/How* or *But/Therefore* · one CTA with *Who/What/When/How* |
| **4. Offer framing** *(when relevant)* | Positions and prices a service | Time, money, and risk as the three value levers · risk reversal · Target → Audit → Gift pitches |

It runs all of this behind the scenes. You get finished copy, not a framework lecture. Where the copy needs a fact only you have, like a real client result, it leaves a `[placeholder]` instead of making one up.

The full skill is in [`skills/copywriting-frameworks/SKILL.md`](skills/copywriting-frameworks/SKILL.md).

## Results: blind-tested on Claude's smallest model

I ran the test on **Claude Haiku 4.5** on purpose. It's Claude's smallest, fastest model, so it brings the least copywriting judgment of its own. If the copy gets better, the skill is doing the work. And Haiku is the model you'd reach for when you're writing copy at volume.

Each of 6 copywriting prompts ran twice, once with the skill and once without. **Claude Sonnet 5** judged every pair blind: two unlabeled outputs in random order, with no way to tell which one had the skill.

| | Without skill | With skill |
|---|---|---|
| Head-to-head wins | 0 | **6** |
| "Usable as-is" score (1–5) | 3.00 | **4.17** |
| Invented facts per output | 1.17 | **0.50** |
| Followed the request | 100% | 100% |

Every score and the judge's reasoning are in [`results/summary.md`](results/summary.md). The test harness, rubric, and raw outputs are in [`evals/`](evals/).

**Keep in mind:**
- **It's a small test.** One run per prompt and one judge. Treat it as a strong signal, not proof.
- **Bigger models haven't been tested on the current version.** An early version, partly run on Sonnet, buried the copy under framework notes. The current version fixes that, and it was tuned on these same 6 prompts. The full story is in [`evals/archive/skill-v1/`](evals/archive/skill-v1/).
- **It invents less, not never.** A couple of numbers still slipped through ("18 months" of runway in the cold email). Check figures before you publish.
- **Test 5 critiques fictional copy** (a made-up SaaS product).

Want to see how it does on a bigger model? The harness runs on your own Claude Code login: `python evals/run.py --models sonnet`.

## Examples

Each folder has the exact prompt plus both Haiku outputs, **without** and **with** the skill.

| Example | What changed with the skill |
|---------|-----------------------------|
| [01 — Hook options](examples/01-hook-options/) | Without the skill, hooks lead with made-up stats ("8+ hours a week", "we asked 500 parents"). With it, they're built on a moment parents actually live, and the one number is flagged as needing real data. |
| [02 — Landing page hero](examples/02-landing-page/) | Without the skill, it invents a coach who "trained 5,000+ first-time marathoners." With it, an honest hero section with no invented credentials. |
| [03 — Cold email](examples/03-cold-email/) | Without the skill, a template-style email with bolded subheads. With it, an email that talks about the founder's runway and ad spend. |
| [04 — CTA rewrite](examples/04-cta-rewrite/) | Without the skill, five fill-in-the-blank templates. With it, one ready-to-use CTA plus versions for other offer types. |
| [05 — Copy critique](examples/05-copy-critique/) | Both spot the vague promise. With the skill, the critique traces it to the root cause (no specific reader) and ends with a concrete next step. |
| [06 — Offer positioning](examples/06-offer-positioning/) | Without the skill, the ad claims "we fixed this for 47 Shopify/Amazon sellers in 2025." With it, the Six P's and the ad make no invented claims. |

## Credit

The frameworks in this skill were distilled and rewritten from **[How To Write Words That Make People Buy (Full Course)](https://youtu.be/OP_eMk_RCWg)** by **Jay Yang** ([@Jayyanginspires](https://x.com/Jayyanginspires) · [YouTube](https://www.youtube.com/@JayYangInspires)), a free copywriting course on YouTube. All the text in this repo is an original summary in my own words. No transcript text is reproduced. If this skill is useful to you, go watch the original.

## License

[MIT](LICENSE)
