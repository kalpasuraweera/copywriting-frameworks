"""Blind A/B grading of with-skill vs without-skill outputs. Safe to re-run: it resumes.

Usage:
    python evals/grade.py                   # LLM judge (default: sonnet)
    python evals/grade.py --human           # write evals/blind-review.md for you to fill in
    python evals/grade.py --human-score     # compare your picks with the judge
"""

import argparse
import json
import random
import re
import sys
from pathlib import Path

from claude_cli import MODELS, ClaudeCallError, run_claude

EVALS = Path(__file__).resolve().parent
RUBRIC = EVALS / "rubric.md"
GRADES = EVALS / "grades"
REVIEW = EVALS / "blind-review.md"
REVIEW_KEY = EVALS / "blind-review-key.json"
AGREEMENT = GRADES / "human-agreement.json"

JUDGE_MESSAGE = """## The request the writer was given

<request>
{prompt}
</request>

## Output A

<output_a>
{a}
</output_a>

## Output B

<output_b>
{b}
</output_b>

Grade both outputs using the rubric in your instructions. Reply with the JSON object only."""


def pairs():
    """Yield (test, model, sample, without_path, with_path) for every complete pair."""
    for without in sorted((EVALS / "runs").glob("*/*/without-skill/run-*.md")):
        with_skill = without.parent.parent / "with-skill" / without.name
        if with_skill.exists():
            test, model = without.parts[-4], without.parts[-3]
            sample = int(without.stem.split("-")[1])
            yield test, model, sample, without, with_skill


def extract_json(text):
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def is_valid(grades):
    return (
        isinstance(grades, dict)
        and isinstance(grades.get("A"), dict)
        and isinstance(grades.get("B"), dict)
        and grades.get("winner") in ("A", "B", "tie")
    )


def judge(judge_model):
    graded = 0
    for test, model, sample, without, with_skill in pairs():
        out = GRADES / test / f"{model}-run-{sample}.json"
        if out.exists():
            continue

        with_is_a = random.Random(f"judge/{test}/{model}/{sample}").random() < 0.5
        a, b = (with_skill, without) if with_is_a else (without, with_skill)
        message = JUDGE_MESSAGE.format(
            prompt=(EVALS / "prompts" / f"{test}.md").read_text(encoding="utf-8").strip(),
            a=a.read_text(encoding="utf-8").strip(),
            b=b.read_text(encoding="utf-8").strip(),
        )

        print(f"JUDGE {test} | {model} | run-{sample} ...", end=" ", flush=True)
        grades, raw = None, ""
        for _ in range(2):
            try:
                result = run_claude(judge_model, RUBRIC, message)
            except ClaudeCallError as err:
                print("STOPPED")
                print(err)
                print("Fix that (or wait for the usage limit to reset), then run the same command to resume.")
                sys.exit(2)
            raw = result["text"]
            grades = extract_json(raw)
            if is_valid(grades):
                break

        record = {
            "test": test,
            "model": model,
            "sample": sample,
            "judge": MODELS[judge_model],
            "key": {
                "A": "with-skill" if with_is_a else "without-skill",
                "B": "without-skill" if with_is_a else "with-skill",
            },
            "valid": is_valid(grades),
            "grades": grades if is_valid(grades) else None,
            "raw": None if is_valid(grades) else raw,
        }
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(record, indent=2), encoding="utf-8")
        graded += 1
        print("done" if record["valid"] else "INVALID JSON (saved raw output, flagged in report)")

    print(f"\nGraded {graded} new pair(s).")


def write_human_review(force):
    if REVIEW.exists() and not force:
        sys.exit(f"{REVIEW.name} already exists (it may have your picks). Use --force to overwrite.")

    items = list(pairs())
    random.Random("human-order").shuffle(items)
    key, sections = {}, []
    for number, (test, model, sample, without, with_skill) in enumerate(items, 1):
        with_is_a = random.Random(f"human/{test}/{model}/{sample}").random() < 0.5
        a, b = (with_skill, without) if with_is_a else (without, with_skill)
        key[str(number)] = {
            "test": test, "model": model, "sample": sample,
            "A": "with-skill" if with_is_a else "without-skill",
            "B": "without-skill" if with_is_a else "with-skill",
        }
        prompt = (EVALS / "prompts" / f"{test}.md").read_text(encoding="utf-8").strip()
        sections.append(
            f"## Pair {number}\n\n**Request:**\n\n````text\n{prompt}\n````\n\n"
            f"### Output A\n\n````text\n{a.read_text(encoding='utf-8').strip()}\n````\n\n"
            f"### Output B\n\n````text\n{b.read_text(encoding='utf-8').strip()}\n````\n\n"
            f"**Your pick (A / B / tie):** \n"
        )

    header = (
        "# Blind review\n\n"
        "Don't open `blind-review-key.json` until you're done. For each pair, read both outputs "
        "and write A, B, or tie after **Your pick**. Judge them as the person who sent the request: "
        "which one would you actually use? Then run `python evals/grade.py --human-score`.\n\n"
    )
    REVIEW.write_text(header + "\n---\n\n".join(sections), encoding="utf-8")
    REVIEW_KEY.write_text(json.dumps(key, indent=2), encoding="utf-8")
    print(f"Wrote {REVIEW.name} with {len(items)} pair(s).")


def score_human():
    key = json.loads(REVIEW_KEY.read_text(encoding="utf-8"))
    text = REVIEW.read_text(encoding="utf-8")
    picks = dict(re.findall(r"## Pair (\d+).*?\*\*Your pick \(A / B / tie\):\*\*[ \t]*(A|B|tie)\b", text, re.S | re.I))

    rows = []
    for number, pick in picks.items():
        info = key[number]
        human = "tie" if pick.lower() == "tie" else info[pick.upper()]
        record_path = GRADES / info["test"] / f"{info['model']}-run-{info['sample']}.json"
        judge_choice = None
        if record_path.exists():
            record = json.loads(record_path.read_text(encoding="utf-8"))
            if record["valid"]:
                winner = record["grades"]["winner"]
                judge_choice = "tie" if winner == "tie" else record["key"][winner]
        rows.append({**info, "human": human, "judge": judge_choice, "agree": human == judge_choice})

    GRADES.mkdir(exist_ok=True)
    AGREEMENT.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    compared = [r for r in rows if r["judge"] is not None]
    agreed = sum(r["agree"] for r in compared)
    print(f"Scored {len(rows)} pick(s). Agreement with judge: {agreed}/{len(compared)}.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--judge", default="sonnet", choices=sorted(MODELS))
    parser.add_argument("--human", action="store_true")
    parser.add_argument("--human-score", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if args.human:
        write_human_review(args.force)
    elif args.human_score:
        score_human()
    else:
        judge(args.judge)


if __name__ == "__main__":
    main()
