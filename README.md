# Copywriting Frameworks — a Claude Skill

A skill that makes Claude think before it writes copy. Before drafting, it works out who the reader is, what they actually get, why they should believe it, and why they should act now. Only then does it write the hook, body, and CTA, in plain, human-sounding prose, without making up stats or testimonials. It's for founders, freelancers, and marketers who write ads, landing pages, emails, and social posts.

## The framework at a glance

| Stage | What it does | Key tools |
|-------|--------------|-----------|
| **1. Think — Six P's** | Answers the strategic questions before any writing | **People** (a specific avatar) · **Positioning** (why you over alternatives) · **Promise** (an outcome, via the "so what?" test) · **Proof** (3 tiers, strongest = a relatable client story) · **Priority** (why now, honestly) · **Process** (how it works, in one line) |
| **2. Write — Five C's** | Sets the prose style | Clear · Concise · Concrete · Conversational · Cadence |
| **3. Structure — Hook / Body / CTA** | Shapes the piece | Hook score ≈ benefit × relevance × credibility ÷ effort · Body as *What/Why/How* or *But/Therefore* · CTA as *Who/What/When/How*, one ask only |
| **4. Offer framing** *(when relevant)* | Positions and prices a service | Three value levers (time, money, risk) · risk reversal · the TAG pitch (Target → Audit → Gift) |

Built-in guardrails: **never invent facts** (missing proof becomes a `[placeholder]`), **finished copy first** (the framework work stays behind the scenes unless you ask for strategy), and **keep the brief's audience**.

The full skill is in [`skills/copywriting-frameworks/SKILL.md`](skills/copywriting-frameworks/SKILL.md).

## Install

**Claude.ai / Claude apps**
Zip the [`skills/copywriting-frameworks/`](skills/copywriting-frameworks/) folder (so the zip contains `copywriting-frameworks/SKILL.md`) and upload it via **Settings → Skills**.

**Claude Code**
Copy the folder into your skills directory:

```bash
# available in every project
cp -r skills/copywriting-frameworks ~/.claude/skills/

# or just one project
cp -r skills/copywriting-frameworks .claude/skills/
```

## Does it actually help? Results

Six copywriting prompts were each run on **Claude Haiku 4.5** twice: once without the skill and once with it. **Claude Sonnet 5** then judged each pair blind. It saw two unlabeled outputs in random order and didn't know which one used the skill.

| | Without skill | With skill |
|---|---|---|
| Head-to-head wins | 0 | **6** |
| "Usable as-is" (1–5, judge) | 3.00 | **4.17** |
| Invented facts per output (avg) | 1.17 | **0.50** |
| Followed the request | 100% | 100% |

Full scores and the judge's reasoning for each test are in [`results/summary.md`](results/summary.md). The harness, rubric, and raw outputs are in [`evals/`](evals/).

**Read these numbers with care:**
- **Small sample.** One run per prompt, one model, one judge model. Treat it as a signal, not proof.
- **Second version, tuned on the same prompts.** The first version of the skill won 5 of 6 on Haiku but only 1 of 4 in a partial Sonnet run. It buried the copy under framework notes and changed the audience in one brief. Those results and the fixes are in [`evals/archive/skill-v1/`](evals/archive/skill-v1/). The current skill was revised using these same 6 prompts, so part of the gain may not carry over to other prompts.
- **It still invents some things.** Fewer than without the skill, but not zero. Examples: "18 months" of runway in the cold email, and a "$2M/year" headline in the bookkeeping ad. Check numbers before you use the copy.
- **Test 5 uses fictional copy.** The copy being critiqued is a made-up SaaS paragraph.

## Examples

Each folder has the exact prompt plus both Haiku outputs, **without** and **with** the skill.

| Example | What changed with the skill |
|---------|-----------------------------|
| [01 — Hook options](examples/01-hook-options/) | Without the skill, the hooks stated made-up stats ("8+ hours a week", "we asked 500 parents"). With it, the hooks are built on the parent's real evening, and the one number is flagged as needing real data. |
| [02 — Landing page hero](examples/02-landing-page/) | Without the skill, it invented a coach who "trained 5,000+ first-time marathoners". With it, the hero section is honest and has no invented credentials. |
| [03 — Cold email](examples/03-cold-email/) | Without the skill: a template-like email with bolded subheads. With it: an email written around the founder's runway and ad spend. |
| [04 — CTA rewrite](examples/04-cta-rewrite/) | Without the skill: five fill-in-the-blank templates. With it: one ready-to-use CTA plus variants for other offer types. |
| [05 — Copy critique](examples/05-copy-critique/) | Both spot the vague promise. With the skill, the critique traces it to the root cause (no specific reader) and gives a concrete next step. |
| [06 — Offer positioning](examples/06-offer-positioning/) | Without the skill, the ad claimed "we fixed this for 47 Shopify/Amazon sellers in 2025". With it, the Six P's and the ad make no invented claims. |

## Credit

The frameworks in this skill were distilled and rewritten from **[How To Write Words That Make People Buy (Full Course)](https://youtu.be/OP_eMk_RCWg)** by **Jay Yang** ([@Jayyanginspires](https://x.com/Jayyanginspires) · [YouTube](https://www.youtube.com/@JayYangInspires)), a free copywriting course on YouTube. All the text in this repo is an original summary in my own words. No transcript text is reproduced. If this skill is useful to you, go watch the original.

## License

[MIT](LICENSE)
