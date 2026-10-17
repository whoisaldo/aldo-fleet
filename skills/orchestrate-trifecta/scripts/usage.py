#!/usr/bin/env python3
"""Print the last usage each fleet gateway saw for the three configured accounts.

The gateways record the rate-limit headers of every response that passes
through them. An account only has fresh numbers if a request went through its
gateway recently, so each line carries the age of its reading. Read-only.
"""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import sys
import time
import urllib.request

# Values are environment-variable names, never original machine addresses or keys.
# Each key file is the user's own JSON file containing a management_key field.
ACCOUNTS = [
    ("max", "coordinator", "TRIFECTA_COORDINATOR_GATEWAY_URL", "TRIFECTA_COORDINATOR_KEY_FILE", "claude"),
    ("builder", "builders", "TRIFECTA_BUILDER_GATEWAY_URL", "TRIFECTA_BUILDER_KEY_FILE", "claude"),
    ("codex", "reviewers", "TRIFECTA_REVIEWER_GATEWAY_URL", "TRIFECTA_REVIEWER_KEY_FILE", "codex"),
]
STALE_MINUTES = 20
MAX_NAP_SECONDS = 110 * 60  # under the two-hour cap on a background command


def latest_reading(auth):
    """The newest non-empty signal set among the account and per-model views."""
    readings = [auth.get("quota") or {}] + list((auth.get("model_quotas") or {}).values())
    readings = [r for r in readings if r.get("signals") and r.get("observed_at")]
    return max(readings, key=lambda r: dt.datetime.fromisoformat(r["observed_at"]), default=None)


def window(used, reset_epoch, now):
    """A used fraction and its reset; a window whose reset has passed is empty."""
    if used is None:
        return None
    reset = dt.datetime.fromtimestamp(int(reset_epoch), dt.timezone.utc) if reset_epoch else None
    if reset and reset <= now:
        return {"used": 0.0, "resets_at": None, "rolled_over": True}
    return {"used": round(float(used), 2), "resets_at": reset.astimezone().isoformat(timespec="minutes") if reset else None}


def summarize(provider, reading, now):
    s = reading["signals"]
    observed = dt.datetime.fromisoformat(reading["observed_at"])
    out = {"age_minutes": int((now - observed).total_seconds() // 60)}
    if provider == "claude":
        out["five_hour"] = window(s.get("Anthropic-Ratelimit-Unified-5h-Utilization"), s.get("Anthropic-Ratelimit-Unified-5h-Reset"), now)
        out["weekly"] = window(s.get("Anthropic-Ratelimit-Unified-7d-Utilization"), s.get("Anthropic-Ratelimit-Unified-7d-Reset"), now)
        out["status"] = s.get("Anthropic-Ratelimit-Unified-Status")
    else:
        used = s.get("X-Codex-Primary-Used-Percent")
        out["weekly"] = window(None if used is None else float(used) / 100, s.get("X-Codex-Primary-Reset-At"), now)
        out["five_hour"] = None
        out["status"] = None
    out["stale"] = out["age_minutes"] > STALE_MINUTES
    return out


def read_accounts(now):
    result = {}
    for name, role, url_env, key_file_env, provider in ACCOUNTS:
        entry = {"role": role}
        try:
            url = os.environ.get(url_env, "").rstrip("/")
            key_file = os.environ.get(key_file_env, "")
            if not url or not key_file:
                entry["error"] = f"configure {url_env} and {key_file_env}"
                result[name] = entry
                continue
            if not url.startswith(("https://", "http://")):
                raise ValueError(f"{url_env} must be an HTTP(S) URL")
            key = json.loads(Path(key_file).expanduser().read_text())["management_key"]
            request = urllib.request.Request(url + "/v0/management/auth-files", headers={"Authorization": "Bearer " + key})
            with urllib.request.urlopen(request, timeout=10) as response:
                files = json.load(response)["files"]
            auth = next(f for f in files if f["provider"] == provider)
            reading = latest_reading(auth)
            entry.update(summarize(provider, reading, now) if reading else {"error": "no reading yet"})
        except Exception as error:  # a down gateway must not stop the coordinator
            entry["error"] = f"{type(error).__name__}: {error}"
        result[name] = entry
    return result


def pct(w):
    if w is None:
        return "none"
    text = f"{round(w['used'] * 100)}%"
    if w.get("rolled_over"):
        return text + " (window reset since the reading)"
    return text + (f", resets {w['resets_at']}" if w.get("resets_at") else "")


def sleep_until_reset(name, accounts):
    """Exit 0 once the window has reopened, 3 if the caller should run this again."""
    resets_at = (accounts[name].get("five_hour") or {}).get("resets_at")
    if not resets_at:
        # No reading, or the window already rolled over: nothing to wait for.
        print(f"{name}: no pending 5-hour reset on record; probe the account now")
        return 0
    remaining = (dt.datetime.fromisoformat(resets_at) - dt.datetime.now().astimezone()).total_seconds() + 60
    nap = max(0, min(remaining, MAX_NAP_SECONDS))
    print(f"{name}: resets {resets_at}; sleeping {int(nap // 60)} min", flush=True)
    time.sleep(nap)
    if remaining > MAX_NAP_SECONDS:
        print(f"{name}: reset still ahead; run this again")
        return 3
    print(f"{name}: the 5-hour window has reopened; probe it and move builders back")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--sleep-until-reset", choices=[a[0] for a in ACCOUNTS], metavar="ACCOUNT",
                        help="Sleep until a minute after ACCOUNT's 5-hour reset, for use as a background clock")
    args = parser.parse_args()
    accounts = read_accounts(dt.datetime.now(dt.timezone.utc))
    if args.sleep_until_reset:
        return sleep_until_reset(args.sleep_until_reset, accounts)
    if args.json:
        print(json.dumps(accounts, indent=2))
        return 0
    for name, a in accounts.items():
        if "error" in a:
            print(f"{name:5} ({a['role']}): unknown, {a['error']}")
            continue
        age = f"read {a['age_minutes']} min ago" + (", STALE" if a["stale"] else "")
        print(f"{name:5} ({a['role']}): 5-hour {pct(a['five_hour'])}; weekly {pct(a['weekly'])}; {age}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
