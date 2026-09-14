# Copywriting Frameworks — a Claude Skill

A skill that makes Claude think before it writes copy. Most AI copy sounds generic because it jumps straight to sentences. This skill has Claude first pin down who the reader is, what they actually get, why they should believe it, and why they should act now. Only then does it draft the hook, body, and CTA, and it edits the result for plain, human-sounding prose. It's for founders, freelancers, and marketers who write ads, landing pages, emails, and social posts and want output they can use, not rewrite.

## The framework at a glance

| Stage | What it does | Key tools |
|-------|--------------|-----------|
| **1. Think — Six P's** | Answers the strategic questions before any writing | **People** (a specific avatar) · **Positioning** (why you over alternatives) · **Promise** (an outcome, via the "so what?" test) · **Proof** (3 tiers, strongest = a relatable client story) · **Priority** (why now, honestly) · **Process** (how it works, in one line) |
| **2. Write — Five C's** | Sets the prose style | Clear · Concise · Concrete · Conversational · Cadence |
| **3. Structure — Hook / Body / CTA** | Shapes the piece | Hook score ≈ benefit × relevance × credibility ÷ effort · Body as *What/Why/How* (educational) or *But/Therefore* (story) · CTA as *Who/What/When/How*, one ask only |
| **4. Offer framing** *(when relevant)* | Positions and prices a service | Three value levers (time, money, risk) · risk reversal · the TAG pitch (Target → Audit → Gift) |

Two guardrails built in: **never invent proof** (missing results and testimonials become `[bracketed placeholders]`), and **sanity-check the offer** (it flags promises the product can't honestly keep).

The full skill is in [`skills/copywriting-frameworks/SKILL.md`](skills/copywriting-frameworks/SKILL.md).

## Install

**Claude.ai / Claude apps**
Zip the [`skills/copywriting-frameworks/`](skills/copywriting-frameworks/) folder (so the zip contains `copywriting-frameworks/SKILL.md`) and upload it via **Settings → Skills**.

**Claude Code**
Copy the `skills/copywriting-frameworks/` folder into your skills directory:

```bash
# available in every project
cp -r skills/copywriting-frameworks ~/.claude/skills/

# or just one project
cp -r skills/copywriting-frameworks .claude/skills/
```

Once installed, it loads automatically whenever you ask for something like "write an ad," "give me hook options," or "critique this landing page."

## Examples

Each folder has the exact prompt (`prompt.md`) and the skill's full response (`output.md`).

| Example | What it shows |
|---------|---------------|
| [01 — Hook options](examples/01-hook-options/) | Five Twitter thread hooks for a meal-kit brand, built around the "5:47pm, nothing's defrosted" moment busy parents know, and scored with the hook formula. |
| [02 — Landing page hero](examples/02-landing-page/) | A marathon plan's hero section. The skill first flags that "6 weeks to a marathon" is unsafe for true beginners, then repositions the page honestly. |
| [03 — Cold email](examples/03-cold-email/) | A pitch to a newly funded founder using Target → Audit → Gift. The email leads with a free homepage rewrite instead of "I write great copy." |
| [04 — CTA rewrite](examples/04-cta-rewrite/) | Why "Feel free to reach out anytime" fails all four CTA checks, plus rewrites for services, software, and newsletters. |
| [05 — Copy critique](examples/05-copy-critique/) | A typical buzzword-heavy SaaS paragraph, diagnosed down to one root cause (no specific reader) and rewritten as "Know what's late before your client does." |
| [06 — Offer positioning](examples/06-offer-positioning/) | Six P's for a $3k/month e-commerce bookkeeping service, plus a sample ad that opens with "Shopify says you made money last month. Your bank account disagrees." |

Proof and product details the prompts didn't provide are left as `[placeholders]` on purpose. The skill is designed not to invent them.

## Credit

The frameworks in this skill were distilled and rewritten from **[VIDEO TITLE](VIDEO_URL)** by **[CREATOR NAME]**, a free copywriting course on YouTube. All the text in this repo is an original summary in my own words. No transcript text is reproduced. If this skill is useful to you, go watch the original.

## License

[MIT](LICENSE)
