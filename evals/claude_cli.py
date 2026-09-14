"""One isolated, headless Claude Code call using the Claude Pro plan login.

Isolation: runs from an empty sandbox folder and skips user settings (hooks,
plugins), skills, MCP servers, tools, and the Claude Code system prompt, so the
model only sees the system prompt file we pass plus the user prompt.
"""

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

MODELS = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-5",
    "opus": "claude-opus-5",
}

SANDBOX = Path(tempfile.gettempdir()) / "copywriting-evals-sandbox"


class ClaudeCallError(RuntimeError):
    """A failure that should stop the whole run (usage limit, auth, bad output)."""


def run_claude(model_alias, system_prompt_file, prompt, timeout=900):
    if os.environ.get("ANTHROPIC_API_KEY"):
        raise ClaudeCallError(
            "ANTHROPIC_API_KEY is set, so Claude Code would bill the API instead of "
            "using the Pro plan. Unset it and run again."
        )

    claude = shutil.which("claude")
    if not claude:
        raise ClaudeCallError("The `claude` CLI was not found on PATH.")

    SANDBOX.mkdir(exist_ok=True)
    if any(SANDBOX.iterdir()):
        raise ClaudeCallError(f"Sandbox folder is not empty: {SANDBOX}")

    model = MODELS[model_alias]
    cmd = [
        claude, "-p",
        "--model", model,
        "--setting-sources", "local",
        "--disable-slash-commands",
        "--strict-mcp-config",
        "--tools", "",
        "--no-session-persistence",
        "--system-prompt-file", str(Path(system_prompt_file).resolve()),
        "--output-format", "json",
    ]

    try:
        proc = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=SANDBOX,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise ClaudeCallError(f"Call timed out after {timeout}s.")

    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError:
        raise ClaudeCallError(
            f"Claude Code did not return JSON (exit code {proc.returncode}).\n"
            f"stdout: {proc.stdout[-1500:]}\nstderr: {proc.stderr[-1500:]}"
        )

    if data.get("is_error") or data.get("subtype") != "success":
        raise ClaudeCallError(
            f"Call failed (status {data.get('api_error_status')}): {data.get('result')}"
        )

    model_usage = data.get("modelUsage") or {}
    if not model_usage.get(model, {}).get("outputTokens"):
        raise ClaudeCallError(
            f"Requested {model}, but modelUsage shows: {sorted(model_usage)}"
        )

    return {
        "text": data.get("result", ""),
        "model": model,
        "stop_reason": data.get("stop_reason"),
        "usage": data.get("usage"),
        "modelUsage": model_usage,
        "duration_ms": data.get("duration_ms"),
    }
