# Evals

Checks whether the skill actually improves Claude's copy. Each test prompt runs on each model twice: once **without** the skill and once **with** it. A separate model then grades the two outputs blind.

## How a run is isolated

Every call goes through Claude Code in headless mode (`claude -p`) on a Claude subscription. The harness refuses to run if `ANTHROPIC_API_KEY` is set, so nothing is billed to the API. Each call:

- runs from an empty sandbox folder, so no project `CLAUDE.md`, settings, or memory are loaded
- uses `--setting-sources local` to skip user settings, which means no hooks and no plugins
- uses `--disable-slash-commands` so no skills load
- uses `--strict-mcp-config` and `--tools ""`, so there are no MCP servers and no tools
- uses `--system-prompt-file` to replace the Claude Code system prompt:
  - **without skill:** `You are a helpful assistant.`
  - **with skill:** the same line, followed by the full `SKILL.md`

The user prompt is the same in both conditions. The generated system prompts are saved in `system/` so you can see exactly what the model got.

## Run it

```bash
python evals/run.py --tests 04 --models haiku   # smoke run
python evals/run.py                             # all tests, Haiku then Sonnet, 1 sample
python evals/grade.py                           # blind LLM judge (Sonnet)
python evals/grade.py --human                   # blind review file for a person
python evals/grade.py --human-score             # compare the person's picks with the judge
python evals/report.py                          # writes results/summary.md
```

Every command can be re-run safely and picks up where it left off. If a usage limit is hit, the script stops. Run the same command again after the limit resets.

## Grading

The judge gets the request and two unlabeled outputs in random order, plus [`rubric.md`](rubric.md). It never sees `SKILL.md` or which condition produced which output. Scores:

- **Craft criteria** (avatar, promise, hook, body, CTA, sounds human). These overlap with what the skill teaches, so they lean in its favor.
- **Neutral criteria** (usable as-is, followed the request, invented facts, length). These carry the headline result together with the head-to-head winner.

## Layout

```
prompts/NN-name.md                                        test prompts (verbatim user messages)
system/                                                   generated system prompts
runs/<test>/<model>/<with-skill|without-skill>/run-N.md   outputs (+ .json metadata)
grades/<test>/<model>-run-N.json                          judge scores + answer key
```
