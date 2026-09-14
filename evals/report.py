"""Build results/summary.md from evals/runs and evals/grades."""

import json
from collections import defaultdict
from pathlib import Path

EVALS = Path(__file__).resolve().parent
REPO = EVALS.parent
SUMMARY = REPO / "results" / "summary.md"
GRADES = EVALS / "grades"

FRAMEWORK = ["avatar", "promise_outcome", "hook", "body_shape", "cta", "sounds_human"]
CONDITIONS = ("without-skill", "with-skill")


def mean(values):
    values = [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return sum(values) / len(values) if values else None


def fmt(value, digits=2):
    return "-" if value is None else f"{value:.{digits}f}"


def pct(flags):
    flags = [f for f in flags if isinstance(f, bool)]
    return "-" if not flags else f"{100 * sum(flags) / len(flags):.0f}%"


def load_records():
    records = []
    for path in sorted(GRADES.glob("*/*.json")):
        records.append(json.loads(path.read_text(encoding="utf-8")))
    return records


def main():
    records = load_records()
    valid = [r for r in records if r["valid"]]
    invalid = [r for r in records if not r["valid"]]

    scores = defaultdict(lambda: defaultdict(list))
    wins = defaultdict(lambda: {"with-skill": 0, "without-skill": 0, "tie": 0})
    per_test = []

    for r in valid:
        g = r["grades"]
        for letter in ("A", "B"):
            cond, s = r["key"][letter], g[letter]
            bucket = scores[(r["model"], cond)]
            bucket["usable"].append(s.get("usable_as_is"))
            bucket["framework"].append(mean([s.get(c) for c in FRAMEWORK]))
            bucket["invented"].append(s.get("invented_facts"))
            bucket["followed"].append(s.get("followed_request"))
            bucket["length"].append(s.get("length_ok"))
        winner = "tie" if g["winner"] == "tie" else r["key"][g["winner"]]
        wins[r["model"]][winner] += 1
        per_test.append((r["test"], r["model"], r["sample"], winner, g.get("reason", "")))

    models = sorted({r["model"] for r in valid}, key=lambda m: ["haiku", "sonnet", "opus"].index(m) if m in ("haiku", "sonnet", "opus") else 99)

    lines = ["# Eval results", ""]
    if not valid:
        lines.append("No graded pairs yet. Run `python evals/run.py`, then `python evals/grade.py`.")
    else:
        judges = sorted({r["judge"] for r in valid})
        lines += [
            f"Graded pairs: **{len(valid)}**. Judge: {', '.join(judges)} (blind, A/B order randomized).",
            "",
            "## Head to head (same model, same prompt, with vs without the skill)",
            "",
            "| Model | With skill wins | Without skill wins | Ties |",
            "|---|---|---|---|",
        ]
        for m in models:
            w = wins[m]
            lines.append(f"| {m} | {w['with-skill']} | {w['without-skill']} | {w['tie']} |")

        lines += [
            "",
            "## Scores",
            "",
            "*Usable as-is* and *invented facts* are the neutral measures. *Framework score* checks the "
            "skill's own criteria, so it naturally favors the skill.",
            "",
            "| Model | Condition | Outputs | Usable as-is (1-5) | Framework score (1-5) | Invented facts (avg) | Followed request | Length OK |",
            "|---|---|---|---|---|---|---|---|",
        ]
        for m in models:
            for cond in CONDITIONS:
                b = scores[(m, cond)]
                lines.append(
                    f"| {m} | {cond} | {len(b['usable'])} | {fmt(mean(b['usable']))} | "
                    f"{fmt(mean(b['framework']))} | {fmt(mean(b['invented']))} | "
                    f"{pct(b['followed'])} | {pct(b['length'])} |"
                )

        lines += [
            "",
            "## Per test",
            "",
            "| Test | Model | Run | Winner | Judge's reason | Outputs |",
            "|---|---|---|---|---|---|",
        ]
        for test, model, sample, winner, reason in sorted(per_test):
            base = f"../evals/runs/{test}/{model}"
            links = f"[with]({base}/with-skill/run-{sample}.md) / [without]({base}/without-skill/run-{sample}.md)"
            reason = reason.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {test} | {model} | {sample} | {winner} | {reason} | {links} |")

    agreement_path = GRADES / "human-agreement.json"
    if agreement_path.exists():
        rows = json.loads(agreement_path.read_text(encoding="utf-8"))
        compared = [r for r in rows if r["judge"] is not None]
        agreed = sum(r["agree"] for r in compared)
        lines += ["", "## Human spot-check", "", f"Blind human picks agreed with the judge on **{agreed}/{len(compared)}** pairs."]

    truncated, skill_hashes = [], set()
    for meta_path in sorted((EVALS / "runs").glob("*/*/*/run-*.json")):
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta["condition"] == "with-skill":
            skill_hashes.add(meta["skill_sha256"])
        if meta["stop_reason"] == "max_tokens":
            truncated.append(meta_path.with_suffix(".md").relative_to(EVALS).as_posix())

    lines += ["", "## Notes", ""]
    if len(skill_hashes) > 1:
        lines.append(f"- WARNING: with-skill runs used {len(skill_hashes)} different SKILL.md versions: {sorted(skill_hashes)}")
    elif skill_hashes:
        lines.append(f"- SKILL.md version (sha256 prefix): `{skill_hashes.pop()}`")
    if truncated:
        lines.append(f"- WARNING: truncated outputs: {', '.join(truncated)}")
    if invalid:
        lines.append(f"- {len(invalid)} judge response(s) were not valid JSON and are excluded.")
    lines.append(
        "- Every output was generated with `claude -p` on a Claude Pro plan, from an empty folder, "
        "with user settings, skills, plugins, MCP servers, tools, and the Claude Code system prompt disabled. "
        "Without-skill system prompt: `You are a helpful assistant.` With-skill: the same line plus the full SKILL.md."
    )

    SUMMARY.parent.mkdir(exist_ok=True)
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {SUMMARY.relative_to(REPO).as_posix()}")


if __name__ == "__main__":
    main()
