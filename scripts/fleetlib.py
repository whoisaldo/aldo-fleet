#!/usr/bin/env python3
"""Fleet deployment and task helpers. Python 3.11+, standard library only."""
import argparse
import contextlib
import csv
import datetime as dt
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import tomllib
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def encode(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def expand(path):
    user_home = Path(os.environ.get("FLEET_USER_HOME", str(Path.home())))
    return user_home / path[2:] if path.startswith("~/") else Path(path)


def state_dir(config):
    default = r"D:\AgentWork\fleet-state" if os.name == "nt" else config["state_dir"]
    return expand(os.environ.get("FLEET_STATE_DIR", default))


def atomic_write(path, text, mode=0o600):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".fleet-", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def allow_windows_user(path):
    """Let the interactive user read private trees created by elevated SSH.

    Python 3.13's mode-0700 Windows ACL grants OWNER RIGHTS. An elevated SSH
    process can create directories owned by Administrators, which excludes the
    same user's ordinary desktop token. Grant that user's SID explicitly.
    """
    if os.name != "nt":
        return
    identity = subprocess.check_output(["whoami.exe", "/user", "/fo", "csv", "/nh"], text=True)
    sid = next(csv.reader(identity.strip().splitlines()))[1]
    if not re.fullmatch(r"S-1-(?:[0-9]+-)*[0-9]+", sid):
        raise ValueError("Could not identify the Windows account SID")
    result = subprocess.run(["icacls.exe", str(path), "/grant:r", f"*{sid}:(OI)(CI)F", "/T", "/C"], capture_output=True, text=True)
    if result.returncode:
        raise ValueError(f"Could not grant the interactive Windows user access to {path}")


def tree_entries(root):
    root = Path(root)
    # Path ordering is case-insensitive on Windows. Sort raw relative parts so
    # the digest stays identical to the original case-sensitive Mac release.
    for path in sorted(root.rglob("*"), key=lambda p: tuple(p.relative_to(root).parts)):
        relative = path.relative_to(root)
        if any(p in {".git", "__pycache__", ".pytest_cache", "node_modules"} for p in relative.parts):
            continue
        if path.is_symlink():
            raise ValueError(f"Source symlink requires review: {path}")
        if path.is_file() and path.name != ".DS_Store":
            yield relative.as_posix(), path


def tree_hash(root):
    h = hashlib.sha256()
    for name, path in tree_entries(root):
        h.update(name.encode() + b"\0" + bytes.fromhex(digest(path)))
    return h.hexdigest()


def profile(config, name):
    p = dict(config["profiles"][name])
    p["home"] = (state_dir(config) / "profiles" / name if os.name == "nt" and p.get("managed") else expand(p.get("windows_home", p["home"]) if os.name == "nt" else p["home"]))
    protected = {expand("~/" + n).resolve() for n in [".codex", ".codex_work", ".claude", ".claude_secondary"]}
    protected |= {expand(v["home"]).resolve() for v in config["profiles"].values() if not v.get("managed")}
    if p.get("managed") and p["home"].resolve() in protected:
        raise ValueError("A managed profile cannot target an existing native account home")
    return p


def deep_merge(existing, managed):
    result = dict(existing)
    for key, value in managed.items():
        result[key] = deep_merge(result.get(key, {}), value) if isinstance(value, dict) else value
    return result


def merge_toml_top(existing, values):
    """Replace only owned top-level keys; preserve every unrelated table/key."""
    if existing.strip():
        parsed = tomllib.loads(existing)
        if all(parsed.get(k) == v for k, v in values.items()):
            return existing
    lines = existing.splitlines(keepends=True)
    boundary = next((i for i, line in enumerate(lines) if line.lstrip().startswith("[")), len(lines))
    seen = set()
    for i in range(boundary):
        match = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=", lines[i])
        if match and match.group(1) in values:
            key = match.group(1)
            lines[i] = f"{key} = {json.dumps(values[key])}\n"
            seen.add(key)
    additions = [f"{k} = {json.dumps(v)}\n" for k, v in values.items() if k not in seen]
    if boundary and not lines[boundary - 1].endswith("\n"):
        lines[boundary - 1] += "\n"
    output = "".join(lines[:boundary] + additions + ["\n"] + lines[boundary:])
    tomllib.loads(output)
    return output


def release(config):
    state = state_dir(config)
    sources = {p.name: p for p in (ROOT / "skills").iterdir() if p.is_dir() and (p / "SKILL.md").exists()}
    lock = ROOT / "skills/external.lock.json"
    for entry in read_json(lock).get("skills", []) if lock.exists() else []:
        src = ROOT / entry["path"] if "path" in entry else expand(entry["local_path"])
        if not src.exists():
            raise ValueError(f"External skill missing: {entry['name']}")
        if tree_hash(src) != entry["sha256"]:
            raise ValueError(f"External skill changed: {entry['name']}. Review and update its lock before releasing.")
        if entry["name"] in sources:
            raise ValueError(f"Duplicate skill name: {entry['name']}")
        sources[entry["name"]] = src
    hashes = {name: tree_hash(path) for name, path in sorted(sources.items())}
    revision = hashlib.sha256(encode(hashes).encode()).hexdigest()[:20]
    target = state / "releases" / revision
    if target.exists():
        verify_release(target)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".staging-", dir=target.parent))
        try:
            for name, src in sources.items():
                for relative, path in tree_entries(src):
                    dest = staging / "skills" / name / relative
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(path, dest)
            atomic_write(staging / "manifest.json", encode({"revision": revision, "skills": hashes}))
            verify_release(staging)
            for path in staging.rglob("*"):
                if path.is_file():
                    path.chmod(0o555 if path.stat().st_mode & 0o111 else 0o444)
            for path in sorted(staging.rglob("*"), reverse=True):
                if path.is_dir():
                    path.chmod(0o555)
            os.rename(staging, target)
            target.chmod(0o555)
        except BaseException:
            # Only our uncommitted staging directory is eligible for cleanup.
            for path in staging.rglob("*"):
                path.chmod(0o700 if path.is_dir() else 0o600)
            staging.chmod(0o700)
            shutil.rmtree(staging)
            raise
    allow_windows_user(target)
    atomic_write(state / "latest-release.json", encode({"revision": revision}))
    return target


def verify_release(path):
    manifest = read_json(path / "manifest.json")
    for name, expected in manifest["skills"].items():
        if tree_hash(path / "skills" / name) != expected:
            raise ValueError(f"Release content differs from its manifest: {name}")
    return manifest


def gateway_config(config, name="personal"):
    return config["gateway"] if name == "personal" else config["additional_gateways"][name]


def gateway_keys(config, name="personal"):
    client = state_dir(config) / "gateway-keys" / (name + ".json")
    path = client if client.exists() or os.name == "nt" else expand(gateway_config(config, name)["runtime_dir"]) / "private/client.json"
    return read_json(path)


def render_profile(config, name, revision):
    p = profile(config, name)
    if not p.get("managed"):
        raise ValueError(f"{name} is an existing native profile and is a read-only deployment target")
    home = p["home"]
    gateway_name = p.get("gateway", "personal")
    key = gateway_keys(config, gateway_name)["api_key"]
    url = gateway_config(config, gateway_name)["url"]
    files = {}
    if p["driver"] == "codex":
        path = home / "config.toml"
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        files[path] = merge_toml_top(old, {"model": p["model"], "model_reasoning_effort": p["effort"], "openai_base_url": url + "/v1", "cli_auth_credentials_store": "file"})
        servers = {"openaiDeveloperDocs": {"url": "https://developers.openai.com/mcp"}}
        blender = expand("~/.local/bin/blender-mcp")
        if os.name != "nt" and blender.exists():
            servers["blender"] = {"command": str(blender), "startup_timeout_sec": 90, "tool_timeout_sec": 600}
        parsed = tomllib.loads(files[path])
        for server, settings in servers.items():
            if server not in parsed.get("mcp_servers", {}):
                files[path] += f"\n[mcp_servers.{server}]\n" + "".join(f"{key} = {json.dumps(value)}\n" for key, value in settings.items())
        files[home / "auth.json"] = encode({"OPENAI_API_KEY": key})
        files[home / "AGENTS.md"] = (ROOT / "AGENTS.md").read_text(encoding="utf-8") + "\nThis is the isolated personal Codex gateway profile. Native ChatGPT features may require the personal-codex profile.\n"
    else:
        path = home / "settings.json"
        old = read_json(path) if path.exists() else {}
        preferences = ROOT / "profiles/claude-common.json"
        managed = read_json(preferences) if preferences.exists() else {}
        personal_preferences = ROOT / "profiles/claude-personal.json"
        if p["identity"] == "personal" and personal_preferences.exists():
            managed = deep_merge(managed, read_json(personal_preferences))
            # Language-server plugins are machine-local; Windows has no Swift toolchain.
            if os.name == "nt":
                managed.get("enabledPlugins", {}).pop("swift-lsp@claude-plugins-official", None)
        managed = deep_merge(managed, {"model": p["model"], "effortLevel": p["effort"], "env": {"ANTHROPIC_BASE_URL": url, "ANTHROPIC_AUTH_TOKEN": key}})
        if p["identity"] == "personal":
            managed["env"]["CODEX_HOME"] = str(expand(config["profiles"]["personal-codex"]["home"]))
        files[path] = encode(deep_merge(old, managed))
        details = "Claude-to-Codex image/3D/computer-use bridges use the native personal Codex home." if p["identity"] == "personal" else "Do not send university task content to a personal or employer account. Cross-provider bridge skills are excluded from this profile."
        files[home / "CLAUDE.md"] = (ROOT / "AGENTS.md").read_text(encoding="utf-8") + f"\nThis is the isolated {p['identity']} Claude gateway profile. {details}\n"
    manifest = verify_release(revision)
    links = {}
    for skill in manifest["skills"]:
        source = revision / "skills" / skill
        if p["driver"] == "codex" and (source / ".claude-only").exists():
            continue
        if p["identity"] != "personal" and (source / ".claude-only").exists():
            continue
        links[home / "skills" / skill] = source
    # Codex installs and upgrades its own built-in skills on every platform.
    # They are not part of a fleet release, including on native macOS clients.
    files[home / ".fleet-profile.json"] = encode({"name": name, "revision": revision.name, "identity": p["identity"], "driver": p["driver"]})
    return p, files, links


def link_matches(path, source):
    if path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction()):
        return path.resolve() == source.resolve()
    if os.name == "nt" and path.is_dir():
        return tree_hash(path) == tree_hash(source)
    return False


def install_skill_link(path, source):
    """Use one canonical skill path, including for Windows Codex discovery."""
    if os.name == "nt":
        # Directory junctions work without Developer Mode or symlink privilege.
        result = subprocess.run(["cmd.exe", "/d", "/c", "mklink", "/J", str(path), str(source)], capture_output=True, text=True)
        if result.returncode:
            raise ValueError(f"Could not create skill junction: {path}")
    else:
        path.symlink_to(source, target_is_directory=True)


def profile_plan(config, name, revision):
    p, files, links = render_profile(config, name, revision)
    changes = {path: text for path, text in files.items() if not path.exists() or path.read_text(encoding="utf-8") != text}
    changed_links = {path: source for path, source in links.items() if not link_matches(path, source)}
    for path in changed_links:
        if path.exists() or path.is_symlink():
            raise ValueError(f"Existing skill is preserved; use a new profile: {path}")
    for path in changes:
        if path.is_symlink():
            raise ValueError(f"Refusing to replace a symlinked profile file: {path}")
    if changes or changed_links:
        for folder in ["sessions", "projects"]:
            path = p["home"] / folder
            if path.exists() and any(path.iterdir()):
                raise ValueError(f"{name} has session history. Create a new profile instead of updating it in place.")
    return p, changes, changed_links


def deploy_profile(config, name, revision, apply=False):
    p, changes, links = profile_plan(config, name, revision)
    if not apply:
        key = gateway_keys(config, p.get("gateway", "personal"))["api_key"]
        for path, text in changes.items():
            old = path.read_text(encoding="utf-8") if path.exists() else ""
            print("".join(difflib.unified_diff(old.replace(key, "<gateway-key>").splitlines(True), text.replace(key, "<gateway-key>").splitlines(True), fromfile=str(path), tofile=str(path))), end="")
        for path, source in links.items():
            print(f"LINK {path} -> {source}")
        return len(changes) + len(links)
    p["home"].mkdir(mode=0o700, parents=True, exist_ok=True)
    p["home"].chmod(0o700)
    backup = state_dir(config) / "backups" / dt.datetime.now().strftime("%Y%m%d-%H%M%S-%f") / name
    for path, text in changes.items():
        if path.exists():
            destination = backup / path.relative_to(p["home"])
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
        atomic_write(path, text)
    for path, source in links.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        install_skill_link(path, source)
    allow_windows_user(p["home"])
    print(f"{name}: {len(changes)} files, {len(links)} skills installed; home {p['home']}")
    return len(changes) + len(links)


def http_json(url, key=None, method="GET", data=None, timeout=15):
    headers = {"Accept": "application/json"}
    if key:
        headers["Authorization"] = "Bearer " + key
    payload = None if data is None else json.dumps(data).encode()
    if payload:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=payload, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def t3_ssh_owned(t3_home):
    """SSH launch states that own the live T3 server. T3's desktop client stops a
    server it marked "managed" whenever its tunnel goes stale, ending every session."""
    runtime = t3_home / "userdata" / "server-runtime.json"
    if not runtime.exists():
        return []
    pid = str(read_json(runtime).get("pid", ""))
    owned = []
    for state in sorted((t3_home / "ssh-launch").glob("*")):
        managed, pid_file = state / "managed", state / "pid"
        if managed.is_file() and managed.read_text().strip() == "managed" and pid_file.is_file() and pid_file.read_text().strip() == pid:
            owned.append(state.name)
    return owned


def doctor(config, selected=None):
    failures = []
    baseline = state_dir(config) / "baseline.json"
    if baseline.exists():
        data = read_json(baseline)
        changed = [p for p, expected in data["files"].items() if not Path(p).is_file() or digest(p) != expected]
        failures += ["Original profile changed: " + p for p in changed]
        print(f"Original profiles: {len(data['files']) - len(changed)}/{len(data['files'])} baseline hashes match")
        runtime = expand("~/.t3/userdata/server-runtime.json")
        same = runtime.exists() and all(read_json(runtime).get(k) == data["t3_runtime"].get(k) for k in ["pid", "startedAt"])
        try:
            current = read_json(runtime)
            port = current.get("port", 3773)
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=5) as response:
                if response.status != 200:
                    raise ValueError("T3 did not return a healthy response")
            print("T3 runtime:", "same server" if same else "reachable; restarted since the initial audit")
        except (OSError, ValueError) as error:
            failures.append(f"T3 is unavailable: {error}")
    for key in t3_ssh_owned(expand("~/.t3")):
        failures.append(
            f"T3 server is owned by a remote SSH client (state {key}), which stops it on reconnect. "
            f"Mark it external: printf 'external\\n' > ~/.t3/ssh-launch/{key}/managed && rm ~/.t3/ssh-launch/{key}/pid"
        )
    for name, raw in config["profiles"].items():
        if not raw.get("managed"):
            continue
        if selected and name not in selected:
            continue
        p = profile(config, name)
        record = p["home"] / ".fleet-profile.json"
        if not record.exists():
            failures.append(f"{name} has not been installed")
            continue
        revision = state_dir(config) / "releases" / read_json(record)["revision"]
        verify_release(revision)
        _, files, links = render_profile(config, name, revision)
        bad = [str(path) for path, source in links.items() if not link_matches(path, source)]
        if bad:
            failures.append(f"{name}: missing or changed skills: {bad}")
        print(f"{name}: release {revision.name}, {len(links)} skills, identity {p['identity']}")
    deployed = state_dir(config) / "skills-deployment.json"
    if deployed.exists():
        record = read_json(deployed)
        revision = state_dir(config) / "releases" / record["release"]
        verify_release(revision)
        for home in record["homes"]:
            for path in (Path(home) / "skills").iterdir():
                if path.name in read_json(revision / "manifest.json")["skills"] and not link_matches(path, revision / "skills" / path.name):
                    failures.append(f"Migrated skill differs: {path}")
        for destination, source in record.get("entries", {}).items():
            path = Path(destination)
            if (source and not link_matches(path, Path(source))) or (source is None and (path.exists() or path.is_symlink())):
                failures.append(f"Migrated skill is missing or changed: {path}")
        print(f"Shared skill migration: {len(record['homes'])} homes, release {revision.name}")
    gateways = {"personal": config["gateway"], **config.get("additional_gateways", {})}
    selected_gateways = {config["profiles"][n].get("gateway", "personal") for n in selected} if selected else set(gateways)
    checked_keys = {}
    for name, gateway in gateways.items():
        if name not in selected_gateways:
            continue
        try:
            keys = gateway_keys(config, name)
            checked_keys[name] = keys["api_key"]
            models = http_json(gateway["url"] + "/v1/models", keys["api_key"])
            counts = {}
            if keys.get("management_key"):
                active_config = http_json(gateway["url"] + "/v0/management/config", keys["management_key"])
                routing = active_config.get("routing", {})
                expected = {"strategy": "fill-first", "session-affinity": True, "session-affinity-ttl": "24h", "session-affinity-subagents": True}
                if any(routing.get(k) != v for k, v in expected.items()):
                    failures.append(f"{name}: session affinity settings differ from fleet configuration")
                auth = http_json(gateway["url"] + "/v0/management/auth-files", keys["management_key"])
                for entry in auth.get("files", []):
                    kind = entry.get("provider", entry.get("type", "unknown"))
                    if not entry.get("disabled", False):
                        counts[kind] = counts.get(kind, 0) + 1
                        expected_email = gateway.get("expected_email")
                        if expected_email and entry.get("email") != expected_email:
                            failures.append(f"{name}: account email does not match its identity")
                for kind in gateway.get("providers", ["claude", "codex"]):
                    if counts.get(kind, 0) != 1:
                        failures.append(f"{name}: exactly one enabled {kind} account is required")
                unexpected = set(counts) - set(gateway.get("providers", ["claude", "codex"]))
                if unexpected:
                    failures.append(f"{name}: unexpected account providers {unexpected}")
            print(f"Gateway {name}: reachable; {len(models.get('data', []))} models; account counts {counts or 'checked on gateway host'}")
            try:
                http_json(gateway["url"] + "/v1/models")
                failures.append(f"{name}: gateway allowed a request without its client key")
            except urllib.error.HTTPError as error:
                if error.code != 401:
                    failures.append(f"{name}: unexpected unauthenticated status {error.code}")
        except (OSError, ValueError, urllib.error.URLError) as error:
            failures.append(f"Gateway {name} check failed: {error}")
    for name, gateway in gateways.items():
        if name not in checked_keys:
            continue
        for other, wrong_key in checked_keys.items():
            if other == name:
                continue
            try:
                http_json(gateway["url"] + "/v1/models", wrong_key)
                failures.append(f"{name}: accepted the {other} identity's client key")
            except urllib.error.HTTPError as error:
                if error.code != 401:
                    failures.append(f"{name}: unexpected cross-identity status {error.code}")
            except urllib.error.URLError as error:
                failures.append(f"{name}: identity isolation check failed: {error}")
    for failure in failures:
        print("PENDING:", failure)
    return 1 if failures else 0


def make_task(config, repo, slug, selected, done):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", slug):
        raise ValueError("Use a lowercase task slug with letters, digits, and hyphens")
    profile(config, selected)
    repo = Path(repo).resolve()
    origin = subprocess.run(["git", "-C", str(repo), "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
    head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    identifier = hashlib.sha256(str(repo).encode()).hexdigest()[:8]
    path = state_dir(config) / "worktrees" / f"{repo.name}-{identifier}" / slug
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "-C", str(repo), "worktree", "add", "-b", "fleet/" + slug, str(path), head], check=True)
    record = {"task": slug, "machine": socket.gethostname(), "profile": selected, "origin": origin, "base": head, "worktree": str(path), "done": done, "created_at": dt.datetime.now(dt.timezone.utc).isoformat()}
    atomic_write(state_dir(config) / "tasks" / f"{identifier}-{slug}.json", encode(record))
    print(encode(record))


@contextlib.contextmanager
def lease(config, resource):
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,40}", resource):
        raise ValueError("Invalid resource name")
    lock = state_dir(config) / "leases" / resource
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        lock.mkdir()
    except FileExistsError:
        raise ValueError(f"Resource already reserved: {lock}. Inspect its owner before removing a stale lease.")
    try:
        atomic_write(lock / "owner.json", encode({"pid": os.getpid(), "host": socket.gethostname(), "started_at": dt.datetime.now(dt.timezone.utc).isoformat()}))
        yield
    finally:
        (lock / "owner.json").unlink(missing_ok=True)
        lock.rmdir()


def run_profile(config, name, arguments):
    p = profile(config, name)
    env = dict(os.environ)
    env["CODEX_HOME" if p["driver"] == "codex" else "CLAUDE_CONFIG_DIR"] = str(p["home"])
    if p.get("managed") and p["driver"] == "claude" and p["identity"] == "personal":
        env["CODEX_HOME"] = str(expand(config["profiles"]["personal-codex"]["home"]))
    runtime = state_dir(config) / "toolchain-runtime.json"
    if not runtime.exists():
        runtime = state_dir(config) / "windows-runtime.json"
    binary = read_json(runtime)[p["driver"]]["binary"] if p.get("managed") and runtime.exists() else shutil.which(p["driver"])
    if not binary and p["driver"] == "claude":
        binary = str(expand("~/.local/bin/claude"))
    if not binary:
        raise ValueError(f"{p['driver']} CLI is not installed")
    return subprocess.call([binary] + arguments, env=env)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    doctor_parser = sub.add_parser("doctor")
    doctor_parser.add_argument("--profile", action="append", help="Check only these installed profiles and their gateways")
    sub.add_parser("release")
    sub.add_parser("profiles")
    for action in ["diff", "apply"]:
        command = sub.add_parser(action)
        command.add_argument("--profile", required=True)
        command.add_argument("--release")
    command = sub.add_parser("run")
    command.add_argument("--profile", required=True)
    command.add_argument("args", nargs=argparse.REMAINDER)
    command = sub.add_parser("task")
    command.add_argument("repo")
    command.add_argument("slug")
    command.add_argument("--profile", required=True)
    command.add_argument("--done", required=True)
    command = sub.add_parser("lease")
    command.add_argument("resource")
    command.add_argument("args", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    config = read_json(ROOT / "fleet.json")
    if args.command == "doctor":
        return doctor(config, args.profile)
    if args.command == "release":
        print(release(config))
    elif args.command == "profiles":
        for name in config["profiles"]:
            p = profile(config, name)
            print(f"{name:24} {p['identity']:14} {p['home']} {'managed' if p.get('managed') else 'native; preserved'}")
    elif args.command in {"diff", "apply"}:
        revision = args.release or read_json(state_dir(config) / "latest-release.json")["revision"]
        if not re.fullmatch(r"[0-9a-f]{20}", revision):
            raise ValueError("Invalid release id")
        deploy_profile(config, args.profile, state_dir(config) / "releases" / revision, apply=args.command == "apply")
    elif args.command == "task":
        make_task(config, args.repo, args.slug, args.profile, args.done)
    else:
        arguments = args.args[1:] if args.args[:1] == ["--"] else args.args
        if args.command == "run":
            return run_profile(config, args.profile, arguments)
        if not arguments:
            raise ValueError("A lease needs a command after --")
        with lease(config, args.resource):
            return subprocess.call(arguments)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print(f"fleet: {error}", file=sys.stderr)
        sys.exit(1)
