#!/usr/bin/env python3
"""Run small, new conversations to measure real gateway cache reuse.

This spends subscription tokens. It never resumes an existing user conversation.
"""
from concurrent.futures import ThreadPoolExecutor
import argparse
import datetime
import json
from pathlib import Path
import subprocess
import uuid

STATE = Path.home() / "Services/fleet"
WORK = STATE / "canary"
BIN = Path.home() / ".local/bin"


def codex_last_request_usage(session, sessions_dir=None):
    """The CLI's turn.completed usage is cumulative across a resumed session."""
    root = sessions_dir or Path.home() / ".codex_fleet/sessions"
    files = list(root.rglob(f"*{session}*.jsonl"))
    if len(files) != 1:
        raise RuntimeError("Cannot identify the verification session's usage log")
    usage = None
    for line in files[0].read_text().splitlines():
        payload = json.loads(line).get("payload", {})
        if payload.get("type") == "token_count":
            usage = payload.get("info", {}).get("last_token_usage") or usage
    if usage is None:
        raise RuntimeError("The verification session did not record request usage")
    return usage


def invoke(args):
    result = subprocess.run(args, cwd=WORK, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=150)
    if result.returncode:
        raise RuntimeError(f"Canary failed, exit {result.returncode}: {(result.stdout or result.stderr)[-1800:]}")
    return result.stdout


def claude_cache(launcher):
    session = str(uuid.uuid4())
    nonce = "fleet-check-" + uuid.uuid4().hex[:12]
    common = [str(BIN / launcher), "--print", "--output-format", "json", "--tools", ""]
    first = json.loads(invoke(common + ["--session-id", session, f"This is an isolated cache verification. Remember this marker: {nonce}. Reply with the marker only. Do not use tools."]))
    second = json.loads(invoke(common + ["--resume", session, "Repeat the exact marker from the preceding turn, and nothing else. Do not use tools."]))
    assert nonce in second.get("result", ""), "Conversation resume lost the marker"
    cached = second["usage"].get("cache_read_input_tokens", 0)
    assert cached > 0, "The resumed Claude request did not report cache-read tokens"
    return {"profile": launcher, "session_id": session, "resumed": True, "first_usage": first["usage"], "second_usage": second["usage"], "cache_read_tokens": cached, "models": list(second.get("modelUsage", {}))}


def codex_cache():
    nonce = "fleet-check-" + uuid.uuid4().hex[:12]
    common = [str(BIN / "codex-fleet"), "exec"]
    first = [json.loads(line) for line in invoke(common + ["--json", "--skip-git-repo-check", "--sandbox", "read-only", f"This is an isolated cache verification. Remember this marker: {nonce}. Reply with the marker only. Do not use tools."]).splitlines() if line.startswith("{")]
    thread = next(e["thread_id"] for e in first if e.get("type") == "thread.started")
    one = codex_last_request_usage(thread)
    second = [json.loads(line) for line in invoke(common + ["resume", "--json", "--skip-git-repo-check", thread, "Repeat the exact marker from the preceding turn, and nothing else. Do not use tools."]).splitlines() if line.startswith("{")]
    texts = [e.get("item", {}).get("text", "") for e in second if e.get("type") == "item.completed"]
    assert any(nonce in text for text in texts), "Conversation resume lost the marker"
    two = codex_last_request_usage(thread)
    assert two.get("cached_input_tokens", 0) > 0, "The resumed Codex request did not report cache-read tokens"
    return {"profile": "codex-fleet", "session_id": thread, "resumed": True, "usage_scope": "last request in each turn", "first_usage": one, "second_usage": two, "cache_read_tokens": two["cached_input_tokens"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", action="append", choices=["fleet-codex", "fleet-claude", "fleet-secondary"], required=True, help="Choose explicitly; each check spends subscription tokens")
    args = parser.parse_args()
    WORK.mkdir(parents=True, exist_ok=True)
    available = {"fleet-claude": lambda: claude_cache("claude-fleet"), "fleet-secondary": lambda: claude_cache("claude-secondary-fleet"), "fleet-codex": codex_cache}
    jobs = {name: available[name] for name in args.profile}
    results = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        pending = {name: executor.submit(job) for name, job in jobs.items()}
        for name, future in pending.items():
            try:
                result = future.result()
                results.append(result)
                print(f"{name}: resumed successfully; {result['cache_read_tokens']} cache-read tokens", flush=True)
            except Exception as error:
                results.append({"profile": name, "error": str(error)})
                print(f"{name}: {error}", flush=True)
    report = {"checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "results": results}
    destination = STATE / "cache-verification.json"
    destination.write_text(json.dumps(report, indent=2) + "\n")
    destination.chmod(0o600)
    print(destination)
    return int(any("error" in item for item in results))


if __name__ == "__main__":
    raise SystemExit(main())
