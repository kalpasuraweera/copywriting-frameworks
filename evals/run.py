"""Generate outputs for every test x model x condition. Safe to re-run: it resumes.

Usage:
    python evals/run.py                              # all tests, haiku then sonnet, 1 sample
    python evals/run.py --tests 04 --models haiku    # smoke run
    python evals/run.py --samples 3                  # top up to 3 samples per cell
"""

import argparse
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from claude_cli import MODELS, ClaudeCallError, run_claude

EVALS = Path(__file__).resolve().parent
REPO = EVALS.parent
SKILL = REPO / "skills" / "copywriting-frameworks" / "SKILL.md"
BASE_SYSTEM = "You are a helpful assistant."
CONDITIONS = ("without-skill", "with-skill")
PLACEHOLDER = "<<PASTE"


def build_system_prompts():
    folder = EVALS / "system"
    folder.mkdir(exist_ok=True)
    skill = SKILL.read_text(encoding="utf-8")
    (folder / "without-skill.txt").write_text(BASE_SYSTEM + "\n", encoding="utf-8")
    (folder / "with-skill.txt").write_text(BASE_SYSTEM + "\n\n" + skill, encoding="utf-8")
    return hashlib.sha256(skill.encode("utf-8")).hexdigest()[:12]


def git_commit():
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True
        )
        return out.stdout.strip() or None
    except OSError:
        return None


def select_tests(arg):
    tests = sorted((EVALS / "prompts").glob("*.md"))
    if arg:
        wanted = [w.strip() for w in arg.split(",")]
        tests = [t for t in tests if any(t.stem.startswith(w) for w in wanted)]
    return tests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tests", help="comma-separated prefixes, e.g. 01,04")
    parser.add_argument("--models", default="haiku,sonnet", help="run in this order")
    parser.add_argument("--samples", type=int, default=1)
    args = parser.parse_args()

    models = [m.strip() for m in args.models.split(",")]
    unknown = [m for m in models if m not in MODELS]
    if unknown:
        sys.exit(f"Unknown model(s): {unknown}. Choose from {sorted(MODELS)}.")

    skill_hash = build_system_prompts()
    commit = git_commit()
    stale = 0

    for model_alias in models:
        for test in select_tests(args.tests):
            prompt = test.read_text(encoding="utf-8")
            if PLACEHOLDER in prompt:
                print(f"SKIP {test.stem}: prompt still has a placeholder to fill in")
                continue

            for sample in range(1, args.samples + 1):
                for condition in CONDITIONS:
                    out = EVALS / "runs" / test.stem / model_alias / condition / f"run-{sample}.md"
                    label = f"{test.stem} | {model_alias} | {condition} | run-{sample}"

                    if out.exists():
                        meta = json.loads(out.with_suffix(".json").read_text(encoding="utf-8"))
                        if condition == "with-skill" and meta.get("skill_sha256") != skill_hash:
                            stale += 1
                        continue

                    print(f"RUN  {label} ...", end=" ", flush=True)
                    try:
                        result = run_claude(model_alias, EVALS / "system" / f"{condition}.txt", prompt)
                    except ClaudeCallError as err:
                        print("STOPPED")
                        print(err)
                        print("Fix that (or wait for the usage limit to reset), then run the same command to resume.")
                        sys.exit(2)

                    out.parent.mkdir(parents=True, exist_ok=True)
                    out.write_text(result["text"], encoding="utf-8")
                    meta = {
                        "test": test.stem,
                        "model_alias": model_alias,
                        "model": result["model"],
                        "condition": condition,
                        "sample": sample,
                        "skill_sha256": skill_hash,
                        "git_commit": commit,
                        "stop_reason": result["stop_reason"],
                        "usage": result["usage"],
                        "modelUsage": result["modelUsage"],
                        "duration_ms": result["duration_ms"],
                        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
                    }
                    out.with_suffix(".json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

                    warning = "  WARNING: truncated (max_tokens)" if result["stop_reason"] == "max_tokens" else ""
                    print(f"done ({(result['duration_ms'] or 0) / 1000:.0f}s){warning}")

    if stale:
        print(
            f"\nWARNING: {stale} existing with-skill run(s) used an older SKILL.md. "
            "Delete them and re-run so results don't mix skill versions."
        )
    print("\nAll requested runs are complete.")


if __name__ == "__main__":
    main()
